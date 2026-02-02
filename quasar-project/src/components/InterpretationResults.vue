<script setup lang="ts">
import { computed } from 'vue'
import type { QTableColumn } from 'quasar'

// Tipo del resultado recibido desde GenesPrediction
type PredictionResult = {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
} | null

type GeneRow = {
  gene: string
  score: number | null
  stresses: string[]
}

const props = defineProps<{ result: PredictionResult }>()

const genesRows = computed(() => {
  if (!props.result?.genes) return []
  return props.result.genes
    .map((g) => {
      if (typeof g === 'string') return { gene: g, score: null, stresses: [] as string[] }
      return { gene: g.gene, score: typeof g.score === 'number' ? g.score : null, stresses: g.stresses ?? [] }
    })
    .filter((g) => g.gene)
})

const geneColumns: QTableColumn<GeneRow>[] = [
  { name: 'gene', label: 'Gen', field: 'gene', align: 'left', sortable: true },
  {
    name: 'score',
    label: 'Score',
    align: 'right',
    sortable: true,
    field: (row) => row.score,
    format: (val) => (typeof val === 'number' ? val.toFixed(3) : '-')
  },
  {
    name: 'stresses',
    label: 'Estrés asociado',
    align: 'left',
    field: (row) => row.stresses,
    format: (val) => (Array.isArray(val) && val.length ? val.join(', ') : '-')
  }
]
</script>

<template>
  <div class="interpretation-results">
    <div class="score-genes-layout">
      <q-card class="score-panel">
        <q-card-section>
          <div class="panel-title">Score (Puntuación)</div>
          <div class="panel-text">
            El Score responde a la pregunta: <strong>¿Qué tan importante fue este gen para recomendar la línea de cultivo ideal para su suelo?</strong>
          </div>
          <div class="panel-text q-mt-sm">
            El valor numérico representa cuánto peso o influencia tuvo la información de este gen en nuestro modelo de predicción para seleccionar la variedad más resiliente a sus condiciones específicas de suelo.
          </div>
          <ul class="score-list">
            <li><strong>Escala:</strong> Los valores van de 0 a 0.03</li>
            <li>Los genes con scores más altos son los que confieren las características de resiliencia más importantes.</li>
          </ul>
        </q-card-section>
      </q-card>

      <q-card class="genes-table-card">
        <q-card-section class="q-pb-none">
          <div class="panel-title">Tabla de genes sugeridos</div>
        </q-card-section>
        <q-card-section class="q-pt-none">
          <q-table
            :rows="genesRows"
            :columns="geneColumns"
            row-key="gene"
            flat
            dense
            bordered
            class="custom-table"
            :rows-per-page-options="[5, 10, 20, 50]"
            :pagination="{ rowsPerPage: 10 }"
          >
            <template v-slot:no-data>
              <div class="full-width row flex-center text-grey q-pa-md">
                <q-icon name="info" size="2em" class="q-mr-sm" />
                <span>No hay genes disponibles en la predicción</span>
              </div>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<style scoped>
.score-genes-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 1024px) {
  .score-genes-layout {
    grid-template-columns: 1fr;
  }
}

.score-panel,
.genes-table-card {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.panel-title {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 6px;
}

.panel-text {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
}

.score-list {
  margin: 12px 0 0 18px;
  padding: 0;
  color: #444;
  font-size: 14px;
  line-height: 1.6;
}

.custom-table {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 8px;
}

.custom-table thead tr {
  background-color: #a9bf6f;
  color: black;
  font-weight: bold;
}
</style>
