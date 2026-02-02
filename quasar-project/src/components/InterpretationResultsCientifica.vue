<script setup lang="ts">
import { computed } from 'vue'

// Tipo del resultado recibido desde GenesPrediction
type PredictionResult = {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score?: number; stresses?: string[] } | string>
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
    <section class="recommendations-panel">
      <!-- Cuadro de recomendaciones de líneas de cultivo -->
      <div class="recommendations-box q-mt-lg">
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
    </section>

    <section class="next-steps-panel">
      <!-- Cuadro de Próximos Pasos -->
      <div class="next-steps-box q-mt-lg">
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
    </section>
  </div>
</template>

<style scoped>
.recommendations-panel {
  width: 100%;
}

.next-steps-panel {
  width: 100%;
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
</style>
