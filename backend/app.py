# ==========================================================
# app.py — Backend FastAPI para predicción de líneas y genes
# ==========================================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib, torch, json
import numpy as np
import pandas as pd
from pathlib import Path

app = FastAPI(title="AbioStress Backend", version="1.0")

# --- CORS: permitir llamadas desde el frontend en dev ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://abio-stress-twas.biorem.cc",
        "http://localhost:9000",  # optional, useful if testing locally
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- rutas base: usa las carpetas del propio proyecto ---
from pathlib import Path
BASE = Path(__file__).resolve().parent
DIR_MODELS  = BASE / "models"
DIR_PREPROC = BASE / "preproc"

def _latest(pattern: str, folder: Path) -> Path:
    folder = Path(folder)
    cands = sorted(folder.glob(pattern))
    if not cands:
        existing = [p.name for p in folder.glob("*")]
        raise FileNotFoundError(
            f"No encontré '{pattern}' en {folder}.\n"
            f"Contenido actual: {existing}"
        )
    return cands[-1]

def _load_model_config(prefix: str):
    """Carga configuración completa para un cultivo (modelo, scaler, metadatos, genes)"""
    try:
        meta_path   = _latest(f"{prefix}_site_meta*.json",      DIR_MODELS)
        panel_path  = _latest(f"{prefix}_line_gene_panel*.json", DIR_MODELS)
        model_path  = _latest(f"{prefix}_site_student*.pt",     DIR_MODELS)
        
        scaler_path = _latest(f"{prefix}_scaler*.joblib",       DIR_PREPROC)
        ohe_path    = _latest(f"{prefix}_ohe*.joblib",          DIR_PREPROC)
        cols_path   = _latest(f"{prefix}_columns*.json",        DIR_PREPROC)
        
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        class_names = meta.get("class_names", [])
        if not class_names:
            raise RuntimeError(f"class_names vacío en meta de {prefix}.")
        
        with open(panel_path, "r", encoding="utf-8") as f:
            gene_panel = json.load(f)
        
        # Cargar scaler y ohe PRIMERO
        scaler = joblib.load(scaler_path)
        ohe = joblib.load(ohe_path)
        
        # Obtener las columnas DIRECTAMENTE del scaler para evitar problemas de encoding
        num_cols = list(scaler.feature_names_in_) if hasattr(scaler, 'feature_names_in_') else []
        
        # Para categóricas, intentar desde el ohe o desde el archivo
        if hasattr(ohe, 'feature_names_in_'):
            cat_cols = list(ohe.feature_names_in_)
        else:
            cols = json.loads(Path(cols_path).read_text(encoding="utf-8"))
            cat_cols = cols.get("categorical", [])
        
        # Dimensiones
        try:
            in_num = getattr(scaler, "n_features_in_", len(num_cols))
        except Exception:
            in_num = len(num_cols)
        
        try:
            ohe_dim = len(ohe.get_feature_names_out())
        except Exception:
            try:
                ohe_dim = int(ohe.transform(pd.DataFrame([{c: "" for c in cat_cols}])).shape[1]) if cat_cols else 0
            except Exception:
                ohe_dim = 0
        
        input_dim = int(in_num + ohe_dim)
        n_classes = int(len(class_names))
        
        return {
            "meta": meta,
            "class_names": class_names,
            "gene_panel": gene_panel,
            "num_cols": num_cols,
            "cat_cols": cat_cols,
            "scaler": scaler,
            "ohe": ohe,
            "input_dim": input_dim,
            "n_classes": n_classes,
            "model_path": model_path,
        }
    except Exception as e:
        raise RuntimeError(f"Error cargando configuración para {prefix}: {e}")

# --- Cargar configuraciones de cultivos disponibles ---
CULTIVOS_CONFIG = {}
CULTIVOS_DISPONIBLES = ["red3", "maiz", "gh"]  # prefijos de archivos

for cultivo_prefix in CULTIVOS_DISPONIBLES:
    try:
        CULTIVOS_CONFIG[cultivo_prefix] = _load_model_config(cultivo_prefix)
    except Exception as e:
        print(f"⚠️ No se pudo cargar {cultivo_prefix}: {e}")

if not CULTIVOS_CONFIG:
    raise RuntimeError("No se pudo cargar ningún modelo de cultivo")

# Mapeo de nombre amigable → prefix de archivo
CULTIVO_MAP = {
    "Sandía": "red3",
    "Maíz": "maiz",
    "Algodón": "gh",
}

# Para compatibilidad con código existente, usar red3 por defecto
META = CULTIVOS_CONFIG["red3"]["meta"]
CLASS_NAMES = CULTIVOS_CONFIG["red3"]["class_names"]
GENE_PANEL = CULTIVOS_CONFIG["red3"]["gene_panel"]
COLS = {"numeric": CULTIVOS_CONFIG["red3"]["num_cols"], "categorical": CULTIVOS_CONFIG["red3"]["cat_cols"]}
NUM_COLS = COLS.get("numeric", [])
CAT_COLS = COLS.get("categorical", [])
INPUT_DIM = CULTIVOS_CONFIG["red3"]["input_dim"]
N_CLASSES = CULTIVOS_CONFIG["red3"]["n_classes"]

import torch.nn as nn

class StudentMLP(nn.Module):
    def __init__(self, in_dim: int, n_classes: int, h1: int = 256, h2: int = 128, p: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, h1),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(h1, h2),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(h2, n_classes),
        )
    def forward(self, x):
        return self.net(x)

def _load_model_any(path: Path, input_dim: int, n_classes: int) -> nn.Module:
    """Carga un modelo PyTorch con las dimensiones especificadas"""
    model = StudentMLP(input_dim, n_classes)
    try:
        payload = torch.load(path, map_location="cpu")
        if isinstance(payload, dict):
            if "model_state_dict" in payload:
                state_dict = payload["model_state_dict"]
            elif "state_dict" in payload:
                state_dict = payload["state_dict"]
            else:
                state_dict = payload
            model.load_state_dict(state_dict, strict=False)
            model.eval()
            return model
    except Exception as e:
        raise RuntimeError(f"No pude cargar state_dict desde {path}: {e}")

    raise RuntimeError("El .pt no contiene ni TorchScript, ni nn.Module, ni state_dict reconocible.")

# Cargar modelos para cada cultivo
MODELOS = {}
for cultivo_prefix, config in CULTIVOS_CONFIG.items():
    try:
        MODELOS[cultivo_prefix] = _load_model_any(
            config["model_path"],
            config["input_dim"],
            config["n_classes"]
        )
    except Exception as e:
        print(f"⚠️ Error cargando modelo para {cultivo_prefix}: {e}")

if not MODELOS:
    raise RuntimeError("No se pudo cargar ningún modelo")

# --- esquema de entrada ---
class SiteInput(BaseModel):
    cultivo: str  # "Sandía" o "Maíz"
    temperatura: float
    humedadRelativa: float
    intensidadLuminica: float
    pH: float
    humedadSuelo: float
    carbonoOrganico: float
    nitrogenoTotal: float
    fosforoSoluble: float
    texturaSuelo: str
    aguaPorcentual: float
    nacl: float
    cd: float
    al: float

def preprocess(inp: SiteInput, cultivo_prefix: str) -> torch.Tensor:
    """Preprocesa entrada para el cultivo especificado"""
    config = CULTIVOS_CONFIG[cultivo_prefix]
    num_cols = config["num_cols"]
    cat_cols = config["cat_cols"]
    scaler = config["scaler"]
    ohe = config["ohe"]
    
    # 1) Convierto el payload a dict simple
    d = inp.dict()

    # 2) Construyo una fila con TODAS las columnas numéricas inicializadas a 0
    row = {col: 0.0 for col in num_cols}
    
    # 3) Identificar columnas de textura (dummies) en el modelo
    TEXTURE_COLUMNS = [c for c in num_cols if any(x in c for x in ["Franco", "Arenoso", "Arcilloso", "Limoso"])]

    # 4) Mapeo inteligente usando coincidencia parcial para campos numéricos
    # Esto evita problemas de encoding de caracteres especiales
    field_mapping = {
        "temperatura": ["temperatura", "temp"],
        "humedadRelativa": ["humedad relativa"],
        "intensidadLuminica": ["intensidad lumin"],
        "pH": ["ph del suelo"],
        "humedadSuelo": ["humedad del suelo"],
        "carbonoOrganico": ["carbono organico"],
        "nitrogenoTotal": ["nitrogeno total"],
        "fosforoSoluble": ["fosforo soluble"],
        "aguaPorcentual": ["peg", "agua"],
        "nacl": ["nacl"],
        "cd": ["cd ("],
        "al": ["al ("],
    }
    
    # 5) Rellenar valores numéricos usando coincidencia de patrones
    for short_key, patterns in field_mapping.items():
        if short_key in d:
            val = d[short_key]
            try:
                val = float(val)
            except Exception:
                val = 0.0
            
            # Buscar y llenar todas las columnas que coincidan
            for col in num_cols:
                if col in TEXTURE_COLUMNS:
                    continue  # Las texturas se manejan por separado
                    
                col_lower = col.lower()
                for pattern in patterns:
                    if pattern.lower() in col_lower:
                        row[col] = val
                        break

    # 6) Mapeo de textura - normalizar el input del usuario
    tex = str(d.get("texturaSuelo", "")).strip().lower()
    
    # Mapeo flexible de textura del usuario a las columnas del modelo
    # El modelo puede tener variaciones como "Franco-arenoso" vs "Arenoso"
    tex_normalized = tex.replace(" ", "-").lower()
    
    # Mapear entrada del usuario a nombres que pueden estar en el modelo
    TEX_VARIANTS = {
        "arenoso": ["Arenoso", "Arenosa"],
        "franco-arenoso": ["Franco-arenoso", "Franco-arenosa", "Franco Arenoso"],
        "franco": ["Franco"],
        "franco-arcilloso": ["Franco-arcilloso", "Franco Arcilloso"],
        "arcilloso": ["Arcilloso", "Arcillosa"],
        "limoso": ["Limoso", "Limosa", "Limosos"],
        "franco-limoso": ["Franco-limoso", "Franco Limoso"],
    }
    
    # Encontrar qué columna del modelo activar
    matched_col = None
    for user_key, model_variants in TEX_VARIANTS.items():
        if tex_normalized == user_key:
            # Buscar cuál de las variantes existe en las columnas del modelo
            for variant in model_variants:
                for c in TEXTURE_COLUMNS:
                    if variant.lower() == c.lower():
                        matched_col = c
                        break
                if matched_col:
                    break
            break
    
    # Activar la columna correspondiente
    for c in TEXTURE_COLUMNS:
        if c in row:
            row[c] = 1.0 if (matched_col and c == matched_col) else 0.0

    # 7) Crea DataFrame CON LOS NOMBRES EXACTOS DE LAS COLUMNAS
    df_num = pd.DataFrame([row], columns=num_cols)

    # 8) Categóricas
    if cat_cols:
        df_cat = pd.DataFrame([{c: "" for c in cat_cols}])
        X_cat = ohe.transform(df_cat)
    else:
        X_cat = np.zeros((1, 0), dtype=np.float32)

    # 9) Escalado
    X_num = scaler.transform(df_num).astype(np.float32)
    X = np.hstack([X_num, X_cat]).astype(np.float32)

    return torch.tensor(X, dtype=torch.float32)

@app.get("/")
def home():
    return {"status": "ok", "msg": "Servidor FastAPI funcionando"}

@app.get("/meta")
def meta():
    return {
        "cultivos": list(CULTIVO_MAP.keys()),
        "class_names": CLASS_NAMES,
        "numeric": NUM_COLS,
        "categorical": CAT_COLS,
    }

#Predicción de línea y genes

@app.post("/predict")
def predict_site(payload: SiteInput):
    try:
        # Determinar cultivo y prefix
        cultivo_nombre = payload.cultivo
        cultivo_prefix = CULTIVO_MAP.get(cultivo_nombre)
        
        if not cultivo_prefix:
            raise HTTPException(
                status_code=400, 
                detail=f"Cultivo no soportado: {cultivo_nombre}. Disponibles: {list(CULTIVO_MAP.keys())}"
            )
        
        if cultivo_prefix not in CULTIVOS_CONFIG:
            raise HTTPException(
                status_code=400,
                detail=f"Modelo no disponible para {cultivo_nombre}"
            )
        
        # Obtener config y modelo
        config = CULTIVOS_CONFIG[cultivo_prefix]
        model = MODELOS[cultivo_prefix]
        class_names = config["class_names"]
        gene_panel = config["gene_panel"]
        
        # Preprocesar
        X = preprocess(payload, cultivo_prefix)
        
        # Predecir
        with torch.no_grad():
            logits = model(X)
            probs = torch.softmax(logits, dim=1).numpy()[0]

        # línea ganadora
        idx = int(np.argmax(probs))
        pred_line = class_names[idx]
        genes = gene_panel.get(pred_line, [])

        used_line = pred_line
        used_genes = genes

        # fallback: si no hay genes, busca la mejor alternativa CON genes
        if not genes:
            for j in np.argsort(probs)[::-1]:  # de mayor a menor prob
                alt_line = class_names[int(j)]
                alt_genes = gene_panel.get(alt_line, [])
                if alt_genes:  # encontramos una con genes
                    used_line = alt_line
                    used_genes = alt_genes
                    break

        return {
            "predicted_line": pred_line,
            "probabilities": {name: float(p) for name, p in zip(class_names, probs)},
            "genes": used_genes,
            "genes_from_line": used_line  # deja claro de dónde salieron
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {e}")


# -----------------------------
# Endpoint para Interpretaciones (Excel estático en servidor)
# -----------------------------
DB_DIR = BASE / 'db'

# Mapeo de cultivos a archivos
INTERPRETATION_FILES = {
    'Sandía': DB_DIR / 'interpretaciones_sandia.xlsx',
    'Maíz': DB_DIR / 'interpretaciones_maiz.xlsx'
}

@app.get('/interpretation/rows')
def get_interpretation_rows(cultivo: Optional[str] = None, q: Optional[str] = None, field: str = 'id'):
    """Sirve filas del Excel de interpretaciones filtradas por cultivo y búsqueda"""
    
    # Determinar qué archivos leer
    files_to_read = []
    if cultivo and cultivo != 'Todos':
        # Leer solo el archivo del cultivo especificado
        file_path = INTERPRETATION_FILES.get(cultivo)
        if file_path and file_path.exists():
            files_to_read.append((cultivo, file_path))
        elif file_path:
            raise HTTPException(status_code=404, detail=f'Archivo de interpretaciones para {cultivo} no encontrado')
    else:
        # Leer todos los archivos disponibles
        for cult, file_path in INTERPRETATION_FILES.items():
            if file_path.exists():
                files_to_read.append((cult, file_path))
    
    if not files_to_read:
        raise HTTPException(status_code=404, detail='No se encontraron archivos de interpretaciones')

    try:
        # Leer y combinar todos los archivos necesarios
        all_rows = []
        for cult, file_path in files_to_read:
            df = pd.read_excel(file_path)
            # normalizar nombres de columnas
            cols_map = {c.lower().strip(): c for c in df.columns}
            def find_col(cands):
                for cand in cands:
                    k = cand.lower()
                    if k in cols_map:
                        return cols_map[k]
                return None

            colID = find_col(['id', 'ID', 'Id', 'id del gen', 'ID del gen'])
            colNombre = find_col(['nombre', 'name', 'Nombre'])
            colFunc = find_col(['funcion', 'función', 'function', 'Función'])

            if colID is None or colNombre is None or colFunc is None:
                raise HTTPException(status_code=400, detail=f'El archivo de {cult} no contiene las columnas necesarias (ID, Nombre, Funcion)')

            # Crear filas con el cultivo asociado
            for _, row in df.iterrows():
                all_rows.append({
                    'id': str(row[colID]).strip() if pd.notna(row[colID]) else '',
                    'nombre': str(row[colNombre]).strip() if pd.notna(row[colNombre]) else '',
                    'funcion': str(row[colFunc]).strip() if pd.notna(row[colFunc]) else '',
                    'cultivo': cult
                })
        
        # Convertir a DataFrame para facilitar filtrado
        df2 = pd.DataFrame(all_rows)
        
        # Obtener cultivos disponibles
        cultivos_disponibles = ['Todos'] + [cult for cult, fp in INTERPRETATION_FILES.items() if fp.exists()]

        # aplicar búsqueda q sobre campo específico
        if q and len(df2) > 0:
            ql = str(q).lower()
            if field not in ['id', 'nombre', 'funcion', 'cultivo']:
                field = 'id'
            df2 = df2[df2[field].str.lower().str.contains(ql, na=False, regex=False)]

        # devolver como lista de dicts
        rows = df2.to_dict(orient='records') if len(df2) > 0 else []
        return {
            'rows': rows,
            'total': len(rows),
            'cultivos': cultivos_disponibles
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al leer el Excel: {e}')