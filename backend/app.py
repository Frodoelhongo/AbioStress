# ==========================================================
# app.py — Backend FastAPI para predicción de líneas y genes
# ==========================================================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, torch, json
import numpy as np
import pandas as pd
from pathlib import Path

app = FastAPI(title="AbioStress Backend", version="1.0")

# --- CORS: permitir llamadas desde el frontend en dev ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en producción limita esto a tu dominio
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

# --- artefactos ---
meta_path   = _latest("red3_site_meta*.json",      DIR_MODELS)
panel_path  = _latest("line_gene_panel*.json",     DIR_MODELS)
model_path  = _latest("red3_site_student*.pt",     DIR_MODELS)

scaler_path = _latest("red3_scaler*.joblib",       DIR_PREPROC)
ohe_path    = _latest("red3_ohe*.joblib",          DIR_PREPROC)
cols_path   = _latest("red3_columns*.json",        DIR_PREPROC)

with open(meta_path, "r", encoding="utf-8") as f:
    META = json.load(f)
CLASS_NAMES = META.get("class_names", [])
if not CLASS_NAMES:
    raise RuntimeError("class_names vacío en meta de Red3.")

with open(panel_path, "r", encoding="utf-8") as f:
    GENE_PANEL = json.load(f)

COLS = json.loads(Path(cols_path).read_text(encoding="utf-8"))
NUM_COLS = COLS.get("numeric", [])
CAT_COLS = COLS.get("categorical", [])

scaler = joblib.load(scaler_path)
ohe    = joblib.load(ohe_path)

# --- dimensiones de entrada y salida a partir de preprocesadores y meta ---
try:
    in_num = getattr(scaler, "n_features_in_", len(NUM_COLS))
except Exception:
    in_num = len(NUM_COLS)

try:
    ohe_dim = len(ohe.get_feature_names_out())  # sklearn >= 1.0
except Exception:
    # fallback para versiones viejas
    try:
        ohe_dim = int(ohe.transform(pd.DataFrame([{c: "" for c in CAT_COLS}])).shape[1]) if CAT_COLS else 0
    except Exception:
        ohe_dim = 0

INPUT_DIM  = int(in_num + ohe_dim)
N_CLASSES  = int(len(CLASS_NAMES))

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

def _load_model_any(path: Path) -> nn.Module:
    # 3) intenta checkpoint/state_dict
    model = StudentMLP(INPUT_DIM, N_CLASSES)
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

model = _load_model_any(model_path)

# --- esquema de entrada ---
class SiteInput(BaseModel):
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

def preprocess(inp: SiteInput) -> torch.Tensor:
    # 1) Convierto el payload a dict simple
    d = inp.dict()

    # 2) Mapa de alias: de tus campos → nombres con los que se entrenó el scaler
    #    Ajusta aquí si ves nombres distintos en /meta
    ALIAS = {
        "temperatura": ["Temperatura (°C)", "Temp (°C)"],  # si existen ambas, rellenamos ambas
        "humedadRelativa": ["Humedad Relativa (%)"],
        "intensidadLuminica": ["Intensidad Lumínica (µmol m⁻² s⁻¹)"],
        "pH": ["pH del Suelo"],
        "humedadSuelo": ["Humedad del suelo (%)"],  # ojo: respeta mayúsculas/minúsculas exactas del meta
        "carbonoOrganico": ["Carbono organico total (%)"],
        "nitrogenoTotal": ["Nitrogeno total (kg/ha)"],
        "fosforoSoluble": ["Fosforo soluble (mg/kg)"],
        "aguaPorcentual": ["PEG/Agua (%)"],
        "nacl": ["NaCl (mM)"],
        "cd": ["Cd (mg/L)"],
        "al": ["Al (mol/L)"],
    }

    # 3) Dummies de textura: en tu meta aparecen como columnas numéricas
    #    Ajusta los nombres EXACTOS según /meta
    TEXTURE_COLUMNS = ["Arenoso", "Franco-arenoso", "Limoso"]  # añade/edita si hay más

    # 4) Construyo una fila con TODAS las columnas numéricas que espera el scaler, inicializadas en 0
    row = {col: 0.0 for col in NUM_COLS}

    # 5) Relleno las columnas mapeadas por alias
    for short_key, target_cols in ALIAS.items():
        if short_key in d:
            val = d[short_key]
            # convierte a float seguro
            try:
                val = float(val)
            except Exception:
                val = 0.0
            for col in target_cols:
                if col in row:
                    row[col] = val  # si existe en NUM_COLS, lo rellenamos

    # 6) Mapeo de textura: pongo 1 en la que corresponda, 0 en las demás
    tex = str(d.get("texturaSuelo", "")).strip().lower()
    # normalizo equivalencias
    TEX_MAP = {
        "arenoso": "Arenosa",
        "franco arenoso": "Franco-arenosa",
        "franco": "Franco",                # si tu meta tuviera "Franco" como dummy
        "franco arcilloso": "Franco Arcilloso",
        "arcilloso": "Arcilloso",
        "limoso": "Limosos",
    }
    tex_col = TEX_MAP.get(tex, None)
    for c in TEXTURE_COLUMNS:
        if c in row:
            row[c] = 1.0 if (tex_col == c) else 0.0

    # 7) Crea DataFrame en el ORDEN EXACTO que espera el scaler
    df_num = pd.DataFrame([[row[c] for c in NUM_COLS]], columns=NUM_COLS)

    # 8) No hay categóricas (según /meta está vacío); si hubiera, construye df_cat similar
    if CAT_COLS:
        df_cat = pd.DataFrame([ {c: "" for c in CAT_COLS} ])
        X_cat = ohe.transform(df_cat)
    else:
        X_cat = np.zeros((1,0), dtype=np.float32)

    # 9) Escalado
    X_num = scaler.transform(df_num).astype(np.float32)
    X = np.hstack([X_num, X_cat]).astype(np.float32)

    # DEBUG opcional
    # print("[DEBUG] row used:", row)
    # print("[DEBUG] X shape:", X.shape, "first 5:", X[0, :5])

    return torch.tensor(X, dtype=torch.float32)

@app.get("/")
def home():
    return {"status": "ok", "msg": "Servidor FastAPI funcionando"}

@app.get("/meta")
def meta():
    return {
        "class_names": CLASS_NAMES,
        "numeric": NUM_COLS,
        "categorical": CAT_COLS,
    }

#Preditión de línea y genes

@app.post("/predict")
def predict_site(payload: SiteInput):
    try:
        X = preprocess(payload)
        with torch.no_grad():
            logits = model(X)
            probs  = torch.softmax(logits, dim=1).numpy()[0]

        # línea ganadora
        idx = int(np.argmax(probs))
        pred_line = CLASS_NAMES[idx]
        genes = GENE_PANEL.get(pred_line, [])

        used_line = pred_line
        used_genes = genes

        # fallback: si no hay genes, busca la mejor alternativa CON genes
        if not genes:
            for j in np.argsort(probs)[::-1]:  # de mayor a menor prob
                alt_line = CLASS_NAMES[int(j)]
                alt_genes = GENE_PANEL.get(alt_line, [])
                if alt_genes:  # encontramos una con genes
                    used_line = alt_line
                    used_genes = alt_genes
                    break

        return {
            "predicted_line": pred_line,
            "probabilities": {name: float(p) for name, p in zip(CLASS_NAMES, probs)},
            "genes": used_genes,
            "genes_from_line": used_line  # deja claro de dónde salieron
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {e}")