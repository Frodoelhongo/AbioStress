# Tablas de interpretación (.xlsx)

El endpoint `GET /interpretation/rows` ahora carga automáticamente todos los archivos con patrón:

- `backend/db/interpretaciones_*.xlsx`
- `backend/db/genes_*.xlsx`
- `db/interpretaciones_*.xlsx`
- `db/genes_*.xlsx`

## Formato requerido por archivo

Cada archivo debe incluir estas columnas (sin importar mayúsculas/minúsculas):

- `ID` (o `id`, `Id`, `id del gen`, `ID del gen`)
- `Anotation` (también acepta `Annotation`, `Anotacion`, `Anotación`)
- `GO`
- `KEGG`

## Cómo agregar 5 tablas nuevas

1. Copia tus archivos a `backend/db/`.
2. Nómbralos con el prefijo `interpretaciones_` o `genes_`.
3. Reinicia el backend.

Ejemplo de 5 archivos:

- `interpretaciones_tomate.xlsx`
- `interpretaciones_sorgo.xlsx`
- `interpretaciones_gh.xlsx` (se muestra como "Algodón")
- `interpretaciones_arroz.xlsx`
- `interpretaciones_trigo.xlsx`

También funciona, por ejemplo:

- `genes_Algodon.xlsx`

Con eso aparecerán automáticamente en el filtro de `Cultivo` del frontend.
