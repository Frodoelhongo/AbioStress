# 🌾 Implementación de Múltiples Modelos - AbioStress

**Fecha**: 13 de Noviembre de 2025  
**Estado**: ✅ Completado

## 📋 Resumen de Cambios

Se ha implementado soporte para múltiples cultivos (Sandía y Maíz) en la aplicación AbioStress, permitiendo que los usuarios seleccionen el cultivo para el cual desean realizar predicciones.

---

## 🗂️ Archivos Modificados

### Backend

#### `backend/app.py` (Cambios Principales)

- ✅ **Nueva función `_load_model_config(prefix)`**: Carga dinámicamente la configuración de cada cultivo
- ✅ **Diccionario `CULTIVOS_CONFIG`**: Almacena todos los modelos, scalers, columnas por cultivo
- ✅ **Diccionario `CULTIVO_MAP`**: Mapeo amigable (`"Sandía"` → `"red3"`, `"Maíz"` → `"maiz"`)
- ✅ **Diccionario `MODELOS`**: Carga automática de modelos PyTorch de cada cultivo
- ✅ **Schema `SiteInput`**: Ahora incluye campo `cultivo: str`
- ✅ **Función `preprocess(inp, cultivo_prefix)`**: Preprocesa datos según el cultivo seleccionado
- ✅ **Endpoint `POST /predict`**: Maneja múltiples cultivos automáticamente
- ✅ **Endpoint `GET /meta`**: Ahora devuelve lista de cultivos disponibles

### Frontend

#### `quasar-project/src/services/gene-model.ts`

- ✅ `SUPPORTED_CROPS` actualizado: `['Sandía', 'Maíz']`
- ✅ `predictGenes()` incluye `cultivo` en el payload
- ✅ `fetchMeta()` devuelve información de cultivos disponibles

#### `quasar-project/src/components/GenesPrediction.vue`

- ✅ Select de cultivo ahora usa `cultivosDisponibles` (lista dinámica)
- ✅ Removido mensaje de advertencia "Solo para Sandía"
- ✅ Botón "Predecir" deshabilitado solo si cultivo no soportado
- ✅ `submitForm()` simplificado - Manejo de errores mejorado

---

## 📁 Archivos Copiados del Disco Externo

### Desde `F:\NN_ZM\models\` → `backend/models/`

```
✓ maiz_site_meta_20251111_132606.json
✓ maiz_site_student_20251111_132606.pt
✓ maiz_line_gene_panel.json
```

### Desde `F:\NN_ZM\preproc\` → `backend/preproc/`

```
✓ maiz_scaler_20251111_131028.joblib
✓ maiz_ohe_20251111_131028.joblib
✓ maiz_columns_20251111_131028.json
```

---

## 🔄 Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario selecciona cultivo (Sandía o Maíz) en frontend  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 2. Frontend envía datos + cultivo → POST /predict           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 3. Backend identifica prefix (red3 o maiz)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 4. Carga config: modelo, scaler, columnas, genes            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 5. Preprocesa datos con configuración específica            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 6. Predice línea y genes con modelo del cultivo             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 7. Devuelve resultados al frontend                          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│ 8. Frontend muestra predicción e interpretación             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Cómo Probar

### Opción 1: Prueba Local con Curl

```bash
# Prueba con Sandía
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cultivo": "Sandía",
    "temperatura": 27,
    "humedadRelativa": 40,
    "intensidadLuminica": 800,
    "pH": 5,
    "humedadSuelo": 10,
    "carbonoOrganico": 1.5,
    "nitrogenoTotal": 0.5,
    "fosforoSoluble": 0.5,
    "texturaSuelo": "Franco Arenoso",
    "aguaPorcentual": 10,
    "nacl": 1,
    "cd": 0.5,
    "al": 0.5
  }'

# Prueba con Maíz
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cultivo": "Maíz",
    "temperatura": 27,
    "humedadRelativa": 40,
    "intensidadLuminica": 800,
    "pH": 5,
    "humedadSuelo": 10,
    "carbonoOrganico": 1.5,
    "nitrogenoTotal": 0.5,
    "fosforoSoluble": 0.5,
    "texturaSuelo": "Franco Arenoso",
    "aguaPorcentual": 10,
    "nacl": 1,
    "cd": 0.5,
    "al": 0.5
  }'
```

### Opción 2: Prueba en el Frontend

1. Abre la aplicación en el navegador
2. Ve a la sección **"Predicción de Genes"**
3. En el dropdown de cultivo, selecciona **"Maíz"**
4. Llena los campos del formulario
5. Haz clic en **"Predecir"**
6. Deberías ver los resultados de la predicción para Maíz

---

## ✨ Características Principales

### ✅ Soporte Multi-Cultivo

- Carga dinámica de modelos según cultivo
- Cada cultivo tiene su propio modelo, scaler, y panel de genes

### ✅ Interfaz Amigable

- Selector de cultivo visible en el formulario
- Mensajes de error claros
- Validación de cultivos soportados

### ✅ Mantenible y Escalable

- Fácil agregar nuevos cultivos (solo copiar archivos)
- Código limpio y modular
- Separación clara entre backend y frontend

---

## 🚀 Cómo Agregar Más Cultivos

Para agregar un nuevo cultivo (ej: Sorgo), sigue estos pasos:

### 1. Backend: Copiar archivos

```bash
# Copiar archivos del disco externo al proyecto
cp /ruta/sorgo_site_meta*.json backend/models/
cp /ruta/sorgo_site_student*.pt backend/models/
cp /ruta/sorgo_line_gene_panel.json backend/models/
cp /ruta/sorgo_scaler*.joblib backend/preproc/
cp /ruta/sorgo_ohe*.joblib backend/preproc/
cp /ruta/sorgo_columns*.json backend/preproc/
```

### 2. Backend: Actualizar `app.py`

```python
# En app.py, línea ~60
CULTIVOS_DISPONIBLES = ["red3", "maiz", "sorgo"]  # ← Agregar "sorgo"

# En app.py, línea ~80
CULTIVO_MAP = {
    "Sandía": "red3",
    "Maíz": "maiz",
    "Sorgo": "sorgo",  # ← Agregar
}
```

### 3. Frontend: Actualizar `gene-model.ts`

```typescript
export const SUPPORTED_CROPS: Cultivo[] = ["Sandía", "Maíz", "Sorgo"];
```

### 4. Frontend: Actualizar tipo

```typescript
export type Cultivo = "Maíz" | "Sorgo" | "Tomate" | "Sandía" | "Algodón";
// Ya incluye Sorgo, solo actualiza el arreglo SUPPORTED_CROPS
```

---

## 📊 Estructura de Datos

### CULTIVOS_CONFIG (Backend)

```python
{
  "red3": {
    "meta": {...},
    "class_names": [...],
    "gene_panel": {...},
    "num_cols": [...],
    "cat_cols": [...],
    "scaler": ScalerObj,
    "ohe": OHEObj,
    "input_dim": int,
    "n_classes": int,
    "model_path": Path,
  },
  "maiz": {
    ...similar...
  }
}
```

### MODELOS (Backend)

```python
{
  "red3": StudentMLP_model,
  "maiz": StudentMLP_model,
}
```

---

## 🔍 Solución de Problemas

### Error: "No encontré 'maiz_site_meta\*.json'"

→ Verifica que los archivos estén en `backend/models/` con el prefijo correcto

### Error: "Cultivo no soportado"

→ Verifica que el cultivo esté en `SUPPORTED_CROPS` en `gene-model.ts`

### Error en preprocesamiento

→ Verifica que las columnas en `maiz_columns.json` sean compatibles

### Error: "model_path is not defined"

→ Verifica que `_load_model_config()` se ejecutó correctamente

---

## 📝 Notas Técnicas

- ✅ Los modelos se cargan al iniciar el servidor (no en cada request)
- ✅ Cada cultivo mantiene su propio estado independiente
- ✅ El scaler y OHE son específicos por cultivo
- ✅ Las columnas del preprocesamiento varían por cultivo
- ✅ El panel de genes es único por cultivo

---

## 📞 Próximos Pasos Opcionales

- [ ] Crear endpoint `GET /cultivos` para listar dinámicamente
- [ ] Agregar más cultivos (Sorgo, Tomate, Algodón)
- [ ] Cachear modelos en memoria para mejorar performance
- [ ] Agregar comparación entre múltiples modelos
- [ ] Implementar logs detallados para debugging
- [ ] Agregar tests unitarios para validación

---

**¡Implementación completada exitosamente! 🎉**
