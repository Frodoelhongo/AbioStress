<script setup lang="ts">
import { computed } from 'vue'

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

const props = defineProps<{ result: PredictionResult }>()

const geneCount = computed(() => props.result?.genes?.length ?? 0)

const geneItems = computed(() => {
  if (!props.result?.genes) return []
  const items = props.result.genes.map((gene, index) => {
    if (typeof gene === 'string') {
      return { key: `${gene}-${index}`, gene, score: undefined, stresses: [] as string[] }
    }
    return {
      key: `${gene.gene}-${index}`,
      gene: gene.gene,
      score: gene.score,
      stresses: gene.stresses ?? []
    }
  })

  return items
    .slice()
    .sort((a, b) => (b.score ?? -Infinity) - (a.score ?? -Infinity))
    .slice(0, 5)
})

</script>

<template>
  <div class="interpretation-results">
    <section class="gene-score-panel">
      <div class="recommendations-box q-mt-lg">
        <div class="recommendations-header">
          <div class="header-text">
            <h3 class="recommendations-title">Panel de Genes y Score</h3>
            <p class="recommendations-subtitle">
              Guia rapida para interpretar la relevancia genetica en la prediccion.
            </p>
          </div>
          <div v-if="geneCount > 0" class="recommendation-chip">
            Genes detectados: <span class="chip-strong">{{ geneCount }}</span>
          </div>
        </div>

        <div class="gene-score-grid">
          <div class="info-card">
            <h4 class="info-title">Genes</h4>
            <p class="info-text">
              Los genes listados son los mas relevantes para la condicion evaluada.
              Su presencia sugiere mecanismos biologicos asociados a tolerancia o sensibilidad.
            </p>
            <div v-if="geneItems.length" class="gene-list">
              <div v-for="item in geneItems" :key="item.key" class="gene-row">
                <div class="gene-main">
                  <div class="gene-name">{{ item.gene }}</div>
                  <div v-if="item.stresses.length" class="gene-meaning">
                    {{ item.stresses.join(', ') }}
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="no-genes">No hay genes disponibles para mostrar.</p>
          </div>
          <div class="info-card">
            <h4 class="info-title">Score</h4>
            <p class="info-text">
              El score indica la fuerza de contribucion de cada gen en la prediccion.
              A mayor score, mayor influencia en el resultado.
            </p>
            <div v-if="geneItems.length" class="score-list">
              <div v-for="item in geneItems" :key="item.key" class="score-row">
                <span v-if="item.score !== undefined" class="gene-score">Score {{ item.score }}</span>
                <span v-else class="gene-score is-muted">Score N/D</span>
              </div>
            </div>
            <p v-else class="no-genes">No hay scores disponibles para mostrar.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.interpretation-results {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  color: #243323;
}

.gene-score-panel {
  width: 100%;
}

.recommendations-box {
  background: linear-gradient(180deg, #f4f7ef 0%, #edf2e7 100%);
  border-radius: 16px;
  padding: 22px 26px 26px;
  box-shadow: 0 18px 32px rgba(35, 52, 32, 0.12);
  border: 1px solid rgba(63, 90, 48, 0.2);
  max-width: 980px;
  margin: 0 auto 26px;
  position: relative;
  overflow: hidden;
}

.recommendations-box::before {
  content: "";
  position: absolute;
  inset: -60px auto auto -40px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(136, 174, 94, 0.25) 0%, rgba(136, 174, 94, 0) 70%);
  pointer-events: none;
}

.recommendations-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.header-text {
  max-width: 520px;
}

.recommendations-title {
  font-family: "Playfair Display", "Times New Roman", serif;
  font-size: 22px;
  font-weight: 700;
  color: #2a3a28;
  margin: 0 0 6px 0;
  letter-spacing: 0.3px;
}

.recommendations-subtitle {
  font-size: 14px;
  color: #4e5f4b;
  margin: 0;
}

.recommendation-chip {
  background: #e0ead7;
  color: #2b4b1f;
  border: 1px solid rgba(60, 90, 45, 0.2);
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.6);
  white-space: nowrap;
}

.chip-strong {
  font-weight: 700;
}

.gene-score-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 18px;
  position: relative;
  z-index: 1;
}

.info-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(22, 32, 18, 0.1);
  box-shadow: 0 10px 20px rgba(18, 29, 16, 0.08);
}

.info-title {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #567056;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.info-text {
  font-size: 14px;
  color: #2f3f2b;
  margin: 0;
  line-height: 1.5;
}

.gene-list {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.gene-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 10px;
  border-radius: 10px;
  background: #f6f9f3;
  border: 1px dashed rgba(45, 60, 38, 0.2);
}

.gene-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gene-name {
  font-size: 14px;
  font-weight: 700;
  color: #2b3b27;
}

.gene-meaning {
  font-size: 12px;
  color: #4e5f4b;
}

.score-list {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.score-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 10px;
  border-radius: 10px;
  background: #f6f9f3;
  border: 1px dashed rgba(45, 60, 38, 0.2);
}



.gene-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.gene-score {
  font-size: 14px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 999px;
  background: #d6f1d9;
  color: #1c4b29;
}

.gene-score.is-muted {
  background: #e7efe1;
  color: #3c5b2f;
}

.gene-stress {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 999px;
  background: #fff2c9;
  color: #6e4f10;
}

.no-genes {
  font-size: 13px;
  color: #7a8574;
  font-style: italic;
  margin: 10px 0 0 0;
}

@media (max-width: 1024px) {
  .recommendations-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .recommendation-chip {
    white-space: normal;
  }
}

@media (max-width: 768px) {
  .gene-score-grid {
    grid-template-columns: 1fr;
  }
}
</style>
