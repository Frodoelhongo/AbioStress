<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { QTableProps } from 'quasar'
import { api } from 'src/services/api'

// Tipo del resultado recibido desde GenesPrediction
type PredictionResult = {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
} | null

// props: result (predicción con genes)
const props = defineProps<{ result: PredictionResult; excelUrl?: string }>()

// filas cargadas desde servidor
const rows = ref<Array<Record<string, unknown>>>([])
const loadError = ref<string | null>(null)
const loading = ref(false)

// Búsqueda y filtros
const search = ref('')
const searchField = ref('id') // id, nombre, funcion
const cultivoFilter = ref('Todos')
const availableCultivos = ref<string[]>(['Todos'])

// Clasificar líneas por probabilidad
const highRecommendation = computed(() => {
  if (!props.result?.probabilities) return []
  return Object.entries(props.result.probabilities)
    .filter(([, prob]) => prob > 0.8)
    .sort((a, b) => b[1] - a[1])
})

const moderateRecommendation = computed(() => {
  if (!props.result?.probabilities) return []
  return Object.entries(props.result.probabilities)
    .filter(([, prob]) => prob >= 0.2 && prob <= 0.8)
    .sort((a, b) => b[1] - a[1])
})

const lowRecommendation = computed(() => {
  if (!props.result?.probabilities) return []
  return Object.entries(props.result.probabilities)
    .filter(([, prob]) => prob < 0.2)
    .sort((a, b) => b[1] - a[1])
})

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

// Top 5 genes con mayor score
const top5Genes = computed(() => {
  if (!props.result?.genes) return []
  const genesWithScore = props.result.genes
    .filter((g): g is { gene: string; score: number; stresses?: string[] } =>
      typeof g === 'object' && 'gene' in g && typeof g.score === 'number'
    )
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
  return genesWithScore
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
  const nombre = typeof row.nombre === 'string' ? row.nombre.toLowerCase().trim() : ''
  return predictedGenes.value.has(id) || predictedGenes.value.has(nombre)
}

// Columnas para la tabla
const columns: QTableProps['columns'] = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'nombre', label: 'Nombre', field: 'nombre', align: 'left', sortable: true },
  { name: 'cultivo', label: 'Cultivo', field: 'cultivo', align: 'left', sortable: true },
  { name: 'funcion', label: 'Función', field: 'funcion', align: 'left' }
]

// Exportar la vista actual (filtrada) a Excel
async function exportFiltered () {
  if (!rows.value.length) return
  const XLSX = await import('xlsx').catch(() => null)
  if (!XLSX) {
    loadError.value = 'Falta la librería "xlsx". Instálala con: npm i xlsx'
    return
  }
  const ws = XLSX.utils.json_to_sheet(rows.value.map(r => ({ ID: r.id, Nombre: r.nombre, Funcion: r.funcion, Cultivo: r.cultivo ?? '' })))
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
    <!-- Cuadro informativo para el agricultor -->
    <div class="farmer-info-box q-mb-lg">
      <p class="farmer-greeting">Estimado agricultor:</p>
      <p class="farmer-text">
        Esta herramienta utiliza ciencia de precisión para analizar las características de su suelo.
        Hemos identificado las líneas de cultivo con mayor potencial de adaptación a sus condiciones específicas,
        junto con los genes responsables de su resiliencia. Considere esta información como una guía técnica
        para optimizar la selección de sus cultivos.
      </p>
    </div>

    <!-- Cuadro de recomendaciones de líneas de cultivo -->
    <div class="recommendations-box q-mb-lg">
      <h3 class="recommendations-title">Líneas de Cultivo Recomendadas</h3>

      <div class="recommendations-grid">
        <!-- Alta Recomendación -->
        <div class="recommendation-column">
          <h4 class="recommendation-category high">ALTA RECOMENDACIÓN (Probabilidad >80%)</h4>
          <p class="recommendation-line"><strong>Significado:</strong> Variedades ideales para sus condiciones de suelo</p>
          <p class="recommendation-line"><strong>Ventaja:</strong> Alto potencial de rendimiento</p>
          <p class="recommendation-line"><strong>Acción:</strong> Primera opción para la próxima siembra</p>
          <div v-if="highRecommendation.length > 0" class="lines-list q-mt-sm">
            <div v-for="[line, prob] in highRecommendation" :key="line" class="line-item">
              <span class="line-name">{{ line }}</span>
              <span class="line-prob">{{ (prob * 100).toFixed(1) }}%</span>
            </div>
          </div>
          <p v-else class="no-lines">No hay líneas en esta categoría</p>
        </div>

        <!-- Recomendación Moderada -->
        <div class="recommendation-column">
          <h4 class="recommendation-category moderate">RECOMENDACIÓN MODERADA (Probabilidad 20-80%)</h4>
          <p class="recommendation-line"><strong>Significado:</strong> Pueden crecer pero requieren manejo especializado</p>
          <p class="recommendation-line"><strong>Ventaja:</strong> Opción viable si no hay disponibles las mejor adaptadas</p>
          <p class="recommendation-line"><strong>Acción:</strong> Necesitan seguimiento técnico y ajustes en el manejo</p>
          <div v-if="moderateRecommendation.length > 0" class="lines-list q-mt-sm">
            <div v-for="[line, prob] in moderateRecommendation" :key="line" class="line-item">
              <span class="line-name">{{ line }}</span>
              <span class="line-prob">{{ (prob * 100).toFixed(1) }}%</span>
            </div>
          </div>
          <p v-else class="no-lines">No hay líneas en esta categoría</p>
        </div>

        <!-- No Recomendado -->
        <div class="recommendation-column">
          <h4 class="recommendation-category low">NO RECOMENDADO (Probabilidad &lt;20%)</h4>
          <p class="recommendation-line"><strong>Significado:</strong> Baja adaptación a sus condiciones de suelo</p>
          <p class="recommendation-line"><strong>Riesgo:</strong> Alta probabilidad de bajos rendimientos</p>
          <p class="recommendation-line"><strong>Acción:</strong> Evitar sembrar para prevenir pérdidas</p>
          <div v-if="lowRecommendation.length > 0" class="lines-list q-mt-sm">
            <div v-for="[line, prob] in lowRecommendation" :key="line" class="line-item">
              <span class="line-name">{{ line }}</span>
              <span class="line-prob">{{ (prob * 100).toFixed(1) }}%</span>
            </div>
          </div>
          <p v-else class="no-lines">No hay líneas en esta categoría</p>
        </div>
      </div>
    </div>

    <!-- Título de la sección de genes -->
    <div class="genes-section-header q-mb-md">
      <h2 class="genes-title">Genes Sugeridos</h2>
      <p class="genes-subtitle">¿Qué significan estos genes?</p>
    </div>

    <!-- Layout con cuadro explicativo a la izquierda y top 5 genes a la derecha -->
    <div class="genes-content-layout q-mb-lg">
      <!-- Cuadro explicativo del ID del Gen (izquierda) -->
      <div class="gene-id-explanation-box">
        <h3 class="gene-id-title">ID del Gen</h3>
        <p class="gene-id-text">
          Cada ID es el código de identificación único de un gen específico. Su estructura general nos cuenta dónde se encuentra y a qué cultivo pertenece.
        </p>
        <ul class="gene-id-list">
          <li class="gene-id-item">
            <strong>Primeras letras</strong> - Identifican la especie del cultivo.
            <ul class="gene-id-sublist">
              <li>Ejemplo para maíz: "Zm" (Zea mays)</li>
              <li>Ejemplo para sandía: "Cl" (Citrullus lanatus)</li>
            </ul>
          </li>
          <li class="gene-id-item">
            <strong>Letra "C" + Número:</strong> Indican el cromosoma donde se localiza el gen.
          </li>
          <li class="gene-id-item">
            <strong>Letra "G" + Número:</strong> Ubicación exacta en el cromosoma.
          </li>
        </ul>

        <h3 class="gene-id-title q-mt-md">Score (Puntuación)</h3>
        <p class="gene-id-text">
          El Score responde a la pregunta: <strong>¿Qué tan importante fue este gen para recomendar la línea de cultivo ideal para su suelo?</strong>
        </p>
        <p class="gene-id-text">
          El valor numérico representa cuánto peso o influencia tuvo la información de este gen en nuestro modelo de predicción para seleccionar la variedad más resiliente a sus condiciones específicas de suelo (niveles de estrés, nutrientes, textura etc.).
        </p>
        <ul class="gene-id-list">
          <li class="gene-id-item">
            <strong>Escala:</strong> Los valores van de 0 a 0.03
          </li>
          <li class="gene-id-item">
            Los genes con scores más altos son los que confieren las características de resiliencia más importantes para sus condiciones específicas de suelo.
          </li>
        </ul>
      </div>

      <!-- Top 5 Genes (derecha) -->
      <div class="top-genes-box">
        <h3 class="top-genes-title">Top 5 Genes Más Relevantes</h3>
        <div v-if="top5Genes.length > 0" class="top-genes-list">
          <div v-for="(gene, index) in top5Genes" :key="gene.gene" class="top-gene-item">
            <div class="gene-rank">{{ index + 1 }}</div>
            <div class="gene-info">
              <div class="gene-id">{{ gene.gene }}</div>
              <div class="gene-score">Score: {{ gene.score.toFixed(3) }}</div>
              <div v-if="gene.stresses && gene.stresses.length > 0" class="gene-stresses">
                <span class="stress-badge" v-for="stress in gene.stresses" :key="stress">{{ stress }}</span>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="no-genes-message">No hay genes disponibles en la predicción</p>
      </div>
    </div>

    <!-- Cuadro de Próximos Pasos -->
    <div class="next-steps-box q-mb-lg q-mt-xl">
      <h3 class="next-steps-title">Próximos Pasos</h3>
      <ol class="next-steps-list">
        <li class="next-step-item">
          Revise las variedades en <span class="color-indicator green">VERDE</span> como primera opción
        </li>
        <li class="next-step-item">
          Consulte con su técnico agrícola para el plan de manejo
        </li>
        <li class="next-step-item">
          Evite las variedades en <span class="color-indicator red">ROJO</span> para minimizar riesgos
        </li>
      </ol>
      <p class="success-message">¡Que tenga una cosecha exitosa!</p>
    </div>

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
          :options="['id', 'nombre', 'funcion']"
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

.farmer-info-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 15px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 95%;
  margin: 0 auto 25px;
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

.farmer-greeting {
  font-size: 17px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.farmer-text {
  font-size: 15px;
  font-weight: 400;
  color: #444;
  margin: 0;
  line-height: 1.6;
  text-align: justify;
}

.recommendations-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 18px 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 95%;
  margin: 0 auto 25px;
}

.recommendations-title {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 16px 0;
  text-align: center;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 1024px) {
  .recommendations-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

.recommendation-column {
  display: flex;
  flex-direction: column;
}

.recommendation-item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.recommendation-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.recommendation-category {
  font-size: 15px;
  font-weight: 700;
  margin: 0 0 8px 0;
  padding: 6px 10px;
  border-radius: 6px;
  display: inline-block;
}

.recommendation-category.high {
  background: #d4edda;
  color: #155724;
}

.recommendation-category.moderate {
  background: #fff3cd;
  color: #856404;
}

.recommendation-category.low {
  background: #f8d7da;
  color: #721c24;
}

.recommendation-line {
  font-size: 14px;
  font-weight: 400;
  color: #444;
  margin: 4px 0;
  line-height: 1.5;
}

.lines-list {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  padding: 10px 12px;
  margin-top: 8px;
}

.line-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.line-item:last-child {
  border-bottom: none;
}

.line-name {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.line-prob {
  font-size: 15px;
  font-weight: 700;
  color: #1976d2;
}

.no-lines {
  font-size: 14px;
  color: #999;
  font-style: italic;
  margin: 10px 0 0 0;
}

/* Sección de genes sugeridos */
.genes-section-header {
  text-align: center;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 15px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 750px;
  margin: 0 auto 20px;
}

.genes-title {
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 5px 0;
}

.genes-subtitle {
  font-size: 16px;
  font-weight: 400;
  color: #666;
  margin: 0;
  font-style: italic;
}

/* Layout de genes: explicación a la izquierda, top 5 a la derecha */
.genes-content-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 20px;
  max-width: 95%;
  margin: 0 auto 40px;
}

@media (max-width: 1024px) {
  .genes-content-layout {
    grid-template-columns: 1fr;
  }
}

/* Cuadro explicativo del ID del Gen */
.gene-id-explanation-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 18px 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.gene-id-title {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.gene-id-text {
  font-size: 15px;
  font-weight: 400;
  color: #444;
  margin: 0 0 15px 0;
  line-height: 1.6;
}

.gene-id-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.gene-id-item {
  font-size: 15px;
  color: #444;
  margin: 10px 0;
  line-height: 1.6;
}

.gene-id-item strong {
  color: #2c3e50;
  font-weight: 600;
}

.gene-id-sublist {
  list-style: disc;
  margin: 5px 0 5px 30px;
  padding: 0;
}

.gene-id-sublist li {
  font-size: 14px;
  color: #555;
  margin: 3px 0;
}

/* Top 5 Genes Box */
.top-genes-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  height: fit-content;
}

.top-genes-title {
  font-size: 17px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 15px 0;
  text-align: center;
  width: 100%;
}

.top-genes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 350px;
}

.top-gene-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px;
  background: rgba(169, 191, 111, 0.1);
  border-radius: 8px;
  border-left: 3px solid #a9bf6f;
}

.gene-rank {
  font-size: 20px;
  font-weight: 700;
  color: #a9bf6f;
  min-width: 30px;
  text-align: center;
}

.gene-info {
  flex: 1;
}

.gene-id {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.gene-score {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.gene-stresses {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}

.stress-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: #e8f5e9;
  color: #2e7d32;
  border-radius: 12px;
  font-weight: 500;
}

.no-genes-message {
  font-size: 14px;
  color: #999;
  font-style: italic;
  text-align: center;
  margin: 20px 0;
  max-width: 350px;
}

/* Cuadro de Próximos Pasos */
.next-steps-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 20px 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 750px;
  margin: 0 auto 25px;
}

.next-steps-title {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 15px 0;
  text-align: center;
}

.next-steps-list {
  list-style: decimal;
  padding-left: 25px;
  margin: 0 0 15px 0;
}

.next-step-item {
  font-size: 15px;
  color: #444;
  margin: 10px 0;
  line-height: 1.6;
}

.color-indicator {
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.color-indicator.green {
  color: #155724;
  background: #d4edda;
}

.color-indicator.red {
  color: #721c24;
  background: #f8d7da;
}

.success-message {
  font-size: 16px;
  font-weight: 600;
  color: #2e7d32;
  text-align: center;
  margin: 15px 0 0 0;
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
