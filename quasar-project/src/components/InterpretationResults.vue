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

</script>

<template>
  <div class="interpretation-results">
    <!-- Cuadro de recomendaciones de líneas de cultivo -->
    <div class="recommendations-box q-mt-lg">
      <div class="recommendations-header">
        <div class="header-text">
          <h3 class="recommendations-title">Panel de Recomendaciones</h3>
          <p class="recommendations-subtitle">
            Resultados basados en condiciones similares a las de su región
          </p>
        </div>
        <div v-if="props.result?.predicted_line" class="recommendation-chip">
          Línea recomendada: <span class="chip-strong">{{ props.result.predicted_line }}</span>
        </div>
      </div>

      <div class="recommendations-legend">
        <span class="legend-pill high">Alta</span>
        <span class="legend-pill moderate">Moderada</span>
        <span class="legend-pill low">No recomendada</span>
      </div>

      <div v-if="props.result?.predicted_line" class="recommendation-hero">
        <div class="hero-tag">Línea recomendada</div>
        <div class="hero-line">{{ props.result.predicted_line }}</div>
        <div class="hero-caption">Mejor ajuste para las condiciones evaluadas</div>
      </div>

      <div v-if="props.result?.context" class="summary-grid">
        <div class="summary-card">
          <span class="summary-label">Cultivo</span>
          <span class="summary-value">{{ props.result.context.cultivo }}</span>
        </div>
        <div class="summary-card">
          <span class="summary-label">Estrés evaluado</span>
          <span class="summary-value">{{ props.result.context.stressLabel }}</span>
        </div>
        <div class="summary-card">
          <span class="summary-label">Tolerancia</span>
          <span class="summary-value">{{ props.result.context.tolerance }}</span>
        </div>
      </div>

      <div v-if="props.result?.context" class="meaning-panel">
        <span class="meaning-title">Significado</span>
        <p class="meaning-text">{{ props.result.context.meaning }}</p>
      </div>

      <div class="recommendations-grid">
        <!-- Alta Recomendación -->
        <div class="recommendation-card high">
          <h4 class="recommendation-category">ALTA RECOMENDACIÓN (Probabilidad >80%)</h4>
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
        <div class="recommendation-card moderate">
          <h4 class="recommendation-category">RECOMENDACIÓN MODERADA (Probabilidad 20-80%)</h4>
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
        <div class="recommendation-card low">
          <h4 class="recommendation-category">NO RECOMENDADO (Probabilidad &lt;20%)</h4>
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

    <!-- Cuadro de Próximos Pasos -->
    <div class="next-steps-box q-mt-lg">
      <div class="next-steps-header">
        <h3 class="next-steps-title">Próximos Pasos</h3>
        <span class="next-steps-tag">Guía rápida</span>
      </div>
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
  </div>
</template>

<style scoped>
.interpretation-results {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  color: #243323;
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

.recommendations-legend {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 16px 0 20px;
}

.recommendation-hero {
  background: linear-gradient(120deg, #dcebd2 0%, #f2f7ed 55%, #ffffff 100%);
  border-radius: 14px;
  padding: 14px 16px;
  border: 1px solid rgba(46, 88, 42, 0.2);
  box-shadow: 0 14px 26px rgba(32, 52, 28, 0.14);
  margin-bottom: 18px;
  display: grid;
  gap: 6px;
}

.hero-tag {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #2f5a2f;
  font-weight: 700;
}

.hero-line {
  font-size: 20px;
  font-weight: 800;
  color: #213220;
}

.hero-caption {
  font-size: 12px;
  color: #4e5f4b;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.summary-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 10px 12px;
  border: 1px solid rgba(22, 32, 18, 0.1);
  box-shadow: 0 8px 18px rgba(18, 29, 16, 0.06);
}

.summary-label {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #6a7865;
  margin-bottom: 4px;
}

.summary-value {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #2a3a28;
}

.meaning-panel {
  background: #ffffff;
  border-radius: 14px;
  padding: 14px 16px;
  border: 1px solid rgba(22, 32, 18, 0.12);
  box-shadow: 0 10px 22px rgba(18, 29, 16, 0.08);
  margin-bottom: 18px;
}

.meaning-title {
  display: block;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #567056;
  font-weight: 700;
  margin-bottom: 6px;
}

.meaning-text {
  font-size: 14px;
  color: #2f3f2b;
  margin: 0;
  line-height: 1.5;
}

.legend-pill {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.4px;
  padding: 6px 12px;
  border-radius: 999px;
  text-transform: uppercase;
}

.legend-pill.high {
  background: #d6f1d9;
  color: #1c4b29;
}

.legend-pill.moderate {
  background: #fff2c9;
  color: #6e4f10;
}

.legend-pill.low {
  background: #f6d6d9;
  color: #6b1f28;
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

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .recommendations-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .recommendation-chip {
    white-space: normal;
  }
}

@media (max-width: 640px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}

.recommendation-card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 12px;
  padding: 16px 16px 18px;
  border: 1px solid rgba(22, 32, 18, 0.08);
  box-shadow: 0 10px 20px rgba(18, 29, 16, 0.08);
  position: relative;
  animation: riseIn 0.5s ease both;
}

.recommendation-card.high {
  border-top: 4px solid #2e7d32;
}

.recommendation-card.moderate {
  border-top: 4px solid #c59a32;
}

.recommendation-card.low {
  border-top: 4px solid #b0464f;
}

.recommendation-card:nth-child(1) {
  animation-delay: 0.04s;
}

.recommendation-card:nth-child(2) {
  animation-delay: 0.08s;
}

.recommendation-card:nth-child(3) {
  animation-delay: 0.12s;
}

.recommendation-category {
  font-size: 14px;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #2f3f2b;
}

.recommendation-line {
  font-size: 13px;
  font-weight: 400;
  color: #4d5b49;
  margin: 4px 0;
  line-height: 1.5;
}

.lines-list {
  background: #f6f9f3;
  border-radius: 10px;
  padding: 10px 12px;
  margin-top: 8px;
  border: 1px dashed rgba(45, 60, 38, 0.2);
}

.line-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  animation: fadeSlide 0.4s ease both;
}

.line-item:nth-child(1) {
  animation-delay: 0.06s;
}

.line-item:nth-child(2) {
  animation-delay: 0.1s;
}

.line-item:nth-child(3) {
  animation-delay: 0.14s;
}

.line-item:last-child {
  border-bottom: none;
}

.line-name {
  font-size: 13px;
  font-weight: 600;
  color: #2b3b27;
}

.line-prob {
  font-size: 14px;
  font-weight: 700;
  color: #2d6a4f;
}

.no-lines {
  font-size: 13px;
  color: #7a8574;
  font-style: italic;
  margin: 10px 0 0 0;
}

.next-steps-box {
  background: linear-gradient(180deg, #ffffff 0%, #f6f8f2 100%);
  border-radius: 16px;
  padding: 22px 26px 24px;
  box-shadow: 0 14px 26px rgba(35, 52, 32, 0.1);
  max-width: 880px;
  margin: 0 auto 25px;
  border: 1px solid rgba(40, 60, 32, 0.15);
}

.next-steps-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.next-steps-title {
  font-family: "Playfair Display", "Times New Roman", serif;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e2e;
  margin: 0;
}

.next-steps-tag {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 999px;
  background: #e7efe1;
  color: #3c5b2f;
}

.next-steps-list {
  list-style: decimal;
  padding-left: 25px;
  margin: 0 0 12px 0;
}

.next-step-item {
  font-size: 14px;
  color: #4c5a49;
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
  background: #d7efd9;
}

.color-indicator.red {
  color: #721c24;
  background: #f6d6d9;
}

.success-message {
  font-size: 15px;
  font-weight: 600;
  color: #2f6c36;
  text-align: center;
  margin: 12px 0 0 0;
}

@keyframes riseIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeSlide {
  from {
    opacity: 0;
    transform: translateX(-6px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
