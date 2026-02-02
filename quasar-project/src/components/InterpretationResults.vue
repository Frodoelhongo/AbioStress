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
</script>

<template>
  <div class="interpretation-results">
    <div class="info-panels-grid q-mb-lg">
      <q-card class="info-panel">
        <q-card-section>
          <div class="panel-title">¿Qué es este panel?</div>
          <div class="panel-text">
            Resume líneas de cultivo recomendadas según la predicción de estrés del suelo.
          </div>
        </q-card-section>
      </q-card>

      <q-card class="info-panel">
        <q-card-section>
          <div class="panel-title">Cómo leer los genes</div>
          <div class="panel-text">
            Los genes con mayor score aportan más a la resiliencia. Revise los Top 5.
          </div>
        </q-card-section>
      </q-card>

      <q-card class="info-panel">
        <q-card-section>
          <div class="panel-title">Siguiente paso</div>
          <div class="panel-text">
            Use las líneas en verde como primera opción y consulte con su técnico.
          </div>
        </q-card-section>
      </q-card>

      <q-card class="info-panel">
        <q-card-section>
          <div class="panel-title">Datos filtrados</div>
          <div class="panel-text">
            Puede filtrar por cultivo y exportar la tabla para su análisis.
          </div>
        </q-card-section>
      </q-card>
    </div>

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

    <!-- Cuadro introductorio a la tabla de genes -->
    <div class="genes-intro-box q-mb-lg">
      <p class="genes-intro-text">
        A continuación se presentan los principales genes que permiten a esta variedad adaptarse exitosamente a las características de su suelo, trabajando en conjunto para garantizar un mejor rendimiento en su parcela.
      </p>
    </div>
  </div>
</template>

<style scoped>
.info-panels-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto 20px;
}

@media (max-width: 1200px) {
  .info-panels-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .info-panels-grid {
    grid-template-columns: 1fr;
  }
}

.info-panel {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.panel-title {
  font-size: 15px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 6px;
}

.panel-text {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}

.farmer-info-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 15px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 95%;
  margin: 0 auto 25px;
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

.genes-intro-box {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 10px;
  padding: 18px 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 95%;
  margin: 0 auto 25px;
}

.genes-intro-text {
  font-size: 15px;
  font-weight: 400;
  color: #444;
  margin: 0;
  line-height: 1.6;
  text-align: center;
}
</style>
