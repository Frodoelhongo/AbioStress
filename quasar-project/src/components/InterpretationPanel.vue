<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { QTableProps } from 'quasar'
import { api } from 'src/services/api'
import InterpretationResultsCientifica from 'src/components/InterpretationResultsCientifica.vue'

// Tipo del resultado recibido desde GenesPrediction
type PredictionResult = {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
  context?: {
    cultivo: string
    stressKey: string
    stressLabel: string
    tolerance: 'Alta' | 'Media' | 'Baja'
    meaning: string
  }
} | null

// props: result (predicción con genes)
const props = defineProps<{ result: PredictionResult; excelUrl?: string }>()

// filas cargadas desde servidor
const rows = ref<Array<Record<string, unknown>>>([])
const loadError = ref<string | null>(null)
const loading = ref(false)

// Búsqueda y filtros
const search = ref('')
const searchField = ref('id') // id, anotation, go, kegg, cultivo
const searchFieldOptions = ['id', 'anotation', 'go', 'kegg', 'cultivo']
const cultivoFilter = ref('Todos')
const availableCultivos = ref<string[]>(['Todos'])


// Genes de la predicción (para resaltar)
const predictedGenes = computed(() => {
  if (!props.result?.genes) return new Set<string>()
  const geneSet = new Set<string>()
  for (const g of props.result.genes) {
    const geneStr = typeof g === 'string' ? g : g.gene
    if (geneStr) geneSet.add(geneStr.toLowerCase().trim())
  }
  return geneSet
})


// Cargar filas desde servidor
async function loadRows() {
  loading.value = true
  loadError.value = null
  try {
    const params: Record<string, string> = {}
    if (cultivoFilter.value && cultivoFilter.value !== 'Todos') {
      params.cultivo = cultivoFilter.value
    }
    if (search.value.trim()) {
      params.q = search.value.trim()
      params.field = searchField.value
    }
    const { data } = await api.get('/interpretation/rows', { params })
    rows.value = data.rows || []
    if (data.cultivos) availableCultivos.value = data.cultivos
  } catch (err: unknown) {
    loadError.value = err instanceof Error && 'response' in err
      ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Error al cargar interpretaciones'
      : 'Error al cargar interpretaciones'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Verificar si una fila debe resaltarse (gene match)
function isHighlighted(row: Record<string, unknown>): boolean {
  const id = typeof row.id === 'string' ? row.id.toLowerCase().trim() : ''
  const annotation = typeof row.anotation === 'string' ? row.anotation.toLowerCase().trim() : ''
  return predictedGenes.value.has(id) || predictedGenes.value.has(annotation)
}

// Columnas para la tabla
const columns: QTableProps['columns'] = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'anotation', label: 'Anotation', field: 'anotation', align: 'left', sortable: true },
  { name: 'go', label: 'GO', field: 'go', align: 'left', sortable: true },
  { name: 'kegg', label: 'KEGG', field: 'kegg', align: 'left', sortable: true }
]

// Exportar la vista actual (filtrada) a Excel
async function exportFiltered () {
  if (!rows.value.length) return
  const XLSX = await import('xlsx').catch(() => null)
  if (!XLSX) {
    loadError.value = 'Falta la librería "xlsx". Instálala con: npm i xlsx'
    return
  }
  const ws = XLSX.utils.json_to_sheet(rows.value.map(r => ({
    ID: r.id,
    Anotation: r.anotation,
    GO: r.go,
    KEGG: r.kegg
  })))
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Filtrada')
  XLSX.writeFile(wb, 'interpretacion_filtrada.xlsx')
}

// Cargar al montar
onMounted(() => {
  void loadRows()
})
</script>

<template>
  <div class="q-pa-md interpretation-panel">
    <interpretation-results-cientifica :result="props.result" />

    <!-- Sección de tabla de interpretación -->
    <div class="interpretation-table-section q-mt-xl">
      <!-- Controles de filtrado y búsqueda -->
    <div class="row items-center q-col-gutter-sm q-mb-md filter-controls">
      <div class="col-12 col-md-3">
        <q-select
          dense outlined
          v-model="cultivoFilter"
          :options="availableCultivos"
          label="Filtrar por cultivo"
          @update:model-value="loadRows"
        />
      </div>

      <div class="col-12 col-md-3">
        <q-select
          dense outlined
          v-model="searchField"
          :options="searchFieldOptions"
          label="Buscar en"
        />
      </div>

      <div class="col-12 col-md-4">
        <q-input
          v-model="search"
          dense outlined
          placeholder="Buscar..."
          @keyup.enter="loadRows"
          clearable
        >
          <template #append>
            <q-icon name="search" class="cursor-pointer" @click="loadRows" />
          </template>
        </q-input>
      </div>

      <div class="col-12 col-md-2">
        <q-btn
          color="primary"
          dense
          class="full-width"
          @click="exportFiltered"
          :disable="!rows.length"
          icon="download"
          label="Exportar"
        />
      </div>
    </div>

    <q-banner v-if="loadError" class="bg-red-2 text-red-10 q-mb-sm" dense>
      <template #avatar><q-icon name="error" /></template>
      {{ loadError }}
    </q-banner>

    <q-banner v-if="predictedGenes.size > 0" class="bg-blue-2 text-blue-10 q-mb-sm" dense>
      <template #avatar><q-icon name="info" /></template>
      Resaltando {{ predictedGenes.size }} genes sugeridos por la predicción
    </q-banner>

    <div class="table-wrap">
      <q-table
        :rows="rows"
        :columns="columns"
        row-key="id"
        flat dense bordered
        class="custom-table"
        :loading="loading"
        :rows-per-page-options="[10, 25, 50, 100]"
        :pagination="{ rowsPerPage: 25 }"
      >
        <template v-slot:body-cell="props">
          <q-td
            :props="props"
            :class="{ 'highlight-gene': isHighlighted(props.row) }"
          >
            {{ props.value }}
          </q-td>
        </template>

        <template v-slot:no-data>
          <div class="full-width row flex-center text-grey q-pa-md">
            <q-icon name="search_off" size="2em" class="q-mr-sm" />
            <span>No se encontraron resultados con los filtros aplicados</span>
          </div>
        </template>
      </q-table>
    </div>
    </div>
  </div>
</template>

<style scoped>
.text-primary { color: #506d2f; }
.custom-table {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.custom-table thead tr {
  background-color: #a9bf6f;
  color: black;
  font-weight: bold;
}
.custom-table tbody tr:nth-child(even) { background-color: #f5f5f5; }
.custom-table tbody tr { background-color: white; }

.interpretation-panel {
  min-height: 60vh;
  max-height: none;
  overflow-y: auto;
}

.interpretation-table-section {
  background: transparent;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
}

.filter-controls {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.table-wrap {
  max-height: calc(85vh - 200px);
  overflow: auto;
  padding-right: 8px;
}
.highlight-gene {
  background-color: #fff9c4 !important;
  font-weight: 600;
  border-left: 3px solid #fbc02d;
}
</style>
