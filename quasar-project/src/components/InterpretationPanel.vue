<script setup lang="ts">
import { ref, computed } from 'vue'
import type { QTableProps } from 'quasar' //  ahora usa "import type"

// Tipo del resultado recibido desde GenesPrediction
type PredictionResult = {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
} | null

//  definimos props y las usamos (aunque sea para validación)
defineProps<{ result: PredictionResult }>()

// Archivo subido (Excel)
const file = ref<File | null>(null)
const rows = ref<Array<{ id: string; nombre: string; funcion: string }>>([])
const loadError = ref<string | null>(null)

// Búsqueda SOLO por ID
const search = ref('')
const filtered = computed(() => {
  if (!search.value) return rows.value
  const q = search.value.toLowerCase()
  return rows.value.filter(r => r.id.toLowerCase().includes(q))
})

// Columnas para la tabla
const columns: QTableProps['columns'] = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'nombre', label: 'Nombre', field: 'nombre', align: 'left' },
  { name: 'funcion', label: 'Función', field: 'funcion', align: 'left' }
]

//  tipo fuerte para el JSON y control de nulos
type ExcelRow = Record<string, string | number | null | undefined>

// Parsear Excel con SheetJS (xlsx)
async function onFileChosen (f: File | null) {
  rows.value = []
  loadError.value = null

  if (!f) return
  file.value = f

  try {
    const XLSX = await import('xlsx').catch(() => null)
    if (!XLSX) {
      loadError.value = 'Falta la librería "xlsx". Instálala con: npm i xlsx'
      return
    }

    const buf = await f.arrayBuffer()
    const wb = XLSX.read(buf, { type: 'array' })
    const sheetName = wb.SheetNames[0]
    const ws = wb.Sheets[sheetName!]
    if (!ws) {
      loadError.value = 'No se encontró ninguna hoja en el archivo.'
      return
    }

    const json = XLSX.utils.sheet_to_json<ExcelRow>(ws, { defval: '' })
    if (!json.length) {
      loadError.value = 'La hoja está vacía.'
      return
    }

    const headers = Object.keys(json[0] ?? {}).map(h => h.toLowerCase().trim())
    const findCol = (cands: string[]) => {
      for (const cand of cands) {
        const idx = headers.indexOf(cand.toLowerCase())
        if (idx !== -1) return Object.keys(json[0]!)[idx]
      }
      return null
    }

    const colID = findCol(['id', 'ID', 'Id'])
    const colNombre = findCol(['nombre', 'name'])
    const colFunc = findCol(['funcion', 'función', 'function'])

    if (!colID || !colNombre || !colFunc) {
      loadError.value = 'El archivo debe incluir columnas: ID, Nombre y Funcion.'
      return
    }

    rows.value = json
      .map(r => ({
        id: String(r[colID] ?? '').trim(),
        nombre: String(r[colNombre] ?? '').trim(),
        funcion: String(r[colFunc] ?? '').trim()
      }))
      .filter(r => r.id)

  } catch {
    loadError.value = 'No se pudo leer el archivo. Verifica que sea .xlsx/.xls válido.'
  }
}
</script>

<template>
  <div class="q-pa-md bg-grey-1">
    <div class="text-h5 text-weight-bold text-primary q-mb-sm">
      Interpretación de resultados
    </div>

    <!-- Subir Excel -->
    <div class="row items-center q-col-gutter-md q-mb-sm">
      <div class="col-12 col-md-6">
        <q-file
          v-model="file"
          label="Sube tu archivo Excel (ID, Nombre, Funcion)"
          outlined dense
          accept=".xlsx,.xls"
          @update:model-value="onFileChosen"
          use-chips
          clearable
        >
          <template #prepend><q-icon name="upload_file" /></template>
        </q-file>
      </div>

      <div class="col-12 col-md-6">
        <div class="row items-center justify-end">
          <div class="col-auto text-weight-medium q-pr-sm">ID GEN</div>
          <q-input
            v-model="search"
            dense outlined rounded
            placeholder="Buscar por ID..."
            style="max-width: 220px"
          >
            <template #append><q-icon name="search" /></template>
          </q-input>
        </div>
      </div>
    </div>

    <q-banner v-if="loadError" class="bg-amber-2 text-amber-10 q-mb-sm" dense>
      {{ loadError }}
    </q-banner>

    <div class="text-subtitle2 text-weight-bold q-mb-xs"></div>

    <q-table
      :rows="filtered"
      :columns="columns"
      row-key="id"
      flat dense bordered
      class="custom-table"
      hide-bottom
      :no-data-label="file ? 'Sin coincidencias' : 'Sube un Excel para comenzar'"
    />
  </div>
</template>

<style scoped>
.text-primary { color: #506d2f; }
.custom-table thead tr {
  background-color: #a9bf6f;
  color: black;
  font-weight: bold;
}
.custom-table tbody tr:nth-child(even) { background-color: #f5f5f5; }
</style>
