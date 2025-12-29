# Añadir un nuevo modelo de cultivo (guía rápida)

Esta guía describe los pasos mínimos para integrar un nuevo cultivo (p. ej. `tomate` o `sandia`) en el backend.

## Archivos necesarios

Colocar en el repo (carpetas `backend/models` y `backend/preproc`):

- `backend/models/<prefix>_site_meta*.json` — metadata, **must** contener `class_names`.
- `backend/models/<prefix>_line_gene_panel*.json` — panel de genes por línea.
- `backend/models/<prefix>_site_student*.pt` — checkpoint PyTorch (state_dict o script).

- `backend/preproc/<prefix>_scaler*.joblib` — StandardScaler/transformador numérico.
- `backend/preproc/<prefix>_ohe*.joblib` — OneHotEncoder para categóricas (si aplica).
- `backend/preproc/<prefix>_columns*.json` — archivo con `numeric` y `categorical` si aplica.

> Recomendación: use un `prefix` short y en minúsculas (ej. `tomate`, `sandia`).

## Pasos para integrar

1. Copia o renombra los archivos dentro del repo:

```bash
# si tus archivos vienen como red3_* y quieres convertir a sandia_
for f in red3_*; do mv "$f" "${f/red3_/sandia_}"; done
# luego moverlos a la carpeta del repo
mv sandia_* backend/models/
mv sandia_* backend/preproc/
```

Si quieres preservar historial, usa `git mv` dentro del repo.

2. Actualiza `backend/app.py`:

- Añade el `prefix` a `CULTIVOS_DISPONIBLES` (lista de prefijos).
- Añade el mapeo amigable en `CULTIVO_MAP` (ej. `"Sandía": "sandia"`).

3. Reinicia el backend:

```bash
uvicorn backend.app:app --reload
```

4. Prueba el endpoint `/predict` con un payload de ejemplo (curl shown en el proyecto). También verifica `/meta`.

## Notas y problemas comunes

- Advertencias de versión de scikit-learn: al cargar `joblib` puede aparecer un `InconsistentVersionWarning` si las versiones difieren entre entrenamiento y entorno actual.
- Si hay mismatch en dimensiones entre preproc y checkpoint, el backend intentará inferir `input_dim` desde el `state_dict` y rellenar con ceros si hace falta. Aun así, la solución más robusta es exportar el preproc y el modelo con la misma versión/formato.
- Errores al cargar el `state_dict` suelen contener info sobre shapes (útil para diagnosticar).

## Commit sugerido

```
git add backend/models/sandia_* backend/preproc/sandia_* backend/app.py backend/docs/README_add_model.md
git commit -m "Add Sandía model artifacts and docs"
```

## Tests (opcional)

- Añadir tests simples que llamen `/meta` y `/predict` y verifiquen HTTP 200 y estructura de la respuesta.

---

Si quieres, hago el commit y añado tests rápidos por ti. ¡Dime cómo prefieres proceder! 🚀
