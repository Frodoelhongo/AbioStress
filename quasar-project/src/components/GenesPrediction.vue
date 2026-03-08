<template>

  <q-splitter v-model="splitterModel" style="height: calc(100vh - 100px)">
    <!-- Izquierda: formulario -->
    <template v-slot:before>
      <div class="prediction-panel form-panel q-pa-md">
        <q-form class="q-gutter-md form-card" @submit="submitForm">
          <!-- Crop selection -->
          <q-select
            v-model="inputModelData.cultivo"
            label="Cultivo"
            :options="cultivosDisponibles"
            outlined dense required
            @update:model-value="onCultivoChange"
          />

          <p class="text-bold q-mt-md">Condiciones ambientales</p>
          <q-input v-model.number="inputModelData.temperatura" label="Temperatura (°C)"
                   type="number" outlined dense required :rules="[num(-10, 50)]" />
          <q-input v-model.number="inputModelData.humedadRelativa" label="Humedad Relativa (%)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.intensidadLuminica"
                   label="Intensidad Lumínica (µmol m⁻² s⁻¹)"
                   type="number" outlined dense required />

          <p class="text-bold">Propiedades fisicoquímicas del suelo</p>
          <q-input v-model.number="inputModelData.pH" label="pH del Suelo"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.humedadSuelo" label="Humedad del Suelo (%)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.carbonoOrganico" label="Carbono Orgánico (%)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.nitrogenoTotal" label="Nitrógeno Total (%)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.fosforoSoluble" label="Fósforo Soluble (mg/kg)"
                   type="number" outlined dense required />
          <q-select v-model="inputModelData.texturaSuelo" label="Textura del Suelo"
                    :options="['Arenoso','Franco Arenoso','Franco','Franco Arcilloso','Arcilloso']"
                    outlined dense required />

          <p class="text-bold">Condiciones de estrés abiótico</p>
          <q-input v-model.number="inputModelData.aguaPorcentual" label="Agua Porcentual (%)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.nacl" label="Conductividad electrica (S/m)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.cd" label="Concentración de Cd (mg/kg)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.al" label="Concentración de Al (mg/kg)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.zn" label="Concentración de Zn (mg/kg)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.fe" label="Concentración de Fe (mg/kg)"
                   type="number" outlined dense required />

          <q-btn
            label="Predecir" color="primary" class="full-width" type="submit"
            :disable="!cultivosDisponibles.includes(inputModelData.cultivo) || loading"
            :loading="loading"
          />
        </q-form>
      </div>
    </template>

    <!-- Derecha: resultados + tabs -->
    <template v-slot:after>
      <div class="prediction-panel results-panel q-pa-md">
        <div class="row items-center justify-between q-mb-md">
          <div class="results-title col-grow">Resultados de la Prediccion</div>
        </div>

        <!-- Resultados de predicción -->

        <div class="q-mt-md">
            <div class="q-pa-md results-card">
              <template v-if="errorMsg">
                <q-banner class="bg-red-2 text-red-10" dense>{{ errorMsg }}</q-banner>
              </template>

              <template v-else-if="result">
                <div class="q-mb-md">
                  <div class="text-subtitle1">
                    Línea de genes predicha: <b>{{ result.predicted_line }}</b>
                  </div>
                </div>

                <div class="q-mb-md">
                  <div class="text-subtitle2 q-mb-xs">Probabilidades</div>
                  <div v-for="(p, name) in result.probabilities" :key="name" class="q-mb-xs">
                    {{ name }}: <b>{{ (p * 100).toFixed(1) }}%</b>
                    <q-linear-progress
                      :value="p" color="primary" track-color="grey-3"
                      size="10px" rounded
                    />
                  </div>
                </div>

                <div>
                  <div class="text-subtitle2 q-mb-xs">Genes Sugeridos (top del panel)</div>
                  <div v-if="result.genes && result.genes.length">
                    <q-list bordered separator>
                      <q-item v-for="(g, i) in result.genes" :key="i">
                        <q-item-section>
                          <div class="row items-center justify-between">
                            <span>{{ typeof g === 'string' ? g : g.gene }}</span>
                            <span v-if="typeof g !== 'string' && g.score !== undefined" class="text-grey-7">
                              score: {{ g.score.toFixed(4) }}
                            </span>
                          </div>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                </div>
              </template>

              <template v-else>
                <p class="text-center text-grey">Los resultados aparecerán aquí</p>
              </template>
            </div>
        </div>
      </div>
    </template>
  </q-splitter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { api } from 'src/services/api'
import {
  predictGenes,
  UnsupportedCropError,
  SUPPORTED_CROPS,
  type GENE_MODEL_INPUTS,
} from 'src/services/gene-model'

const emit = defineEmits<{
  'prediction-updated': [result: {
    predicted_line: string
    probabilities: Record<string, number>
    genes: Array<{ gene: string; score: number; stresses: string[] } | string>
    context: {
      cultivo: string
      stressKey: string
      stressLabel: string
      tolerance: 'Alta' | 'Media' | 'Baja'
      meaning: string
    }
  } | null]
}>()

type StressKey = 'NaCl' | 'Cd' | 'Al' | 'Sequía' | 'Sin estrés'

const splitterModel = ref(50)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const result = ref<null | {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score: number; stresses: string[] } | string>
  context: {
    cultivo: string
    stressKey: string
    stressLabel: string
    tolerance: 'Alta' | 'Media' | 'Baja'
    meaning: string
  }
}>(null)

// (Tabs removidas)

// Cultivos disponibles
const cultivosDisponibles = SUPPORTED_CROPS

function onCultivoChange() {
  // Aquí puedes agregar lógica si necesitas cambiar valores al cambiar cultivo
  // Por ahora no es necesario
}

// Form defaults
const inputModelData = ref<GENE_MODEL_INPUTS>({
  cultivo: 'Sandía',
  temperatura:38,
  humedadRelativa: 56,
  intensidadLuminica: 320,
  pH: 7.5,
  humedadSuelo: 0,
  carbonoOrganico: 0.2,
  nitrogenoTotal: 0.03,
  fosforoSoluble: 3.0,
  texturaSuelo: 'Arcilloso',
  aguaPorcentual: 5,
  nacl: 0,
  cd: 37,
  al: 0,
  zn: 0,
  fe: 0,
})


const num =
  (min: number | null, max: number | null, msg = 'Fuera de rango') =>
  (v: unknown) => {
    if (v === '' || v === undefined || v === null || isNaN(v as number)) return 'Número requerido'
    const x = Number(v)
    if (min !== null && x < min) return msg + ` (≥ ${min})`
    if (max !== null && x > max) return msg + ` (≤ ${max})`
    return true
  }

// Acción al enviar el formulario
async function submitForm() {
  errorMsg.value = null
  result.value = null

  try {
    loading.value = true

    type GeneObj = { gene: string; score?: number; stresses?: string[] }
    function isGeneObj(x: unknown): x is GeneObj {
      if (typeof x !== 'object' || x === null) return false
      const r = x as Record<string, unknown>
      return typeof r.gene === 'string'
    }

    const data = await predictGenes(inputModelData.value)

    const stressInfo = (() => {
      const stressMeta: Record<StressKey, { label: string; tolerance: 'Alta' | 'Media' | 'Baja'; meaning: string }> = {
        NaCl: {
          label: 'Salinidad (NaCl)',
          tolerance: 'Alta',
          meaning: 'Buen desempeño con salinidad moderada.',
        },
        Cd: {
          label: 'Metal pesado (Cd)',
          tolerance: 'Alta',
          meaning: 'Resiste suelos con cadmio.',
        },
        Al: {
          label: 'Aluminio (Al)',
          tolerance: 'Alta',
          meaning: 'Mantiene rendimiento con aluminio.',
        },
        Sequía: {
          label: 'Déficit hídrico',
          tolerance: 'Alta',
          meaning: 'Se adapta a baja disponibilidad de agua.',
        },
        'Sin estrés': {
          label: 'Condición general',
          tolerance: 'Media',
          meaning: 'Rendimiento estable en condiciones estándar.',
        },
      }

      const activeFromInputs: StressKey[] = []
      if (inputModelData.value.nacl >= 5) activeFromInputs.push('NaCl')
      if (inputModelData.value.cd >= 1) activeFromInputs.push('Cd')
      if (inputModelData.value.al >= 1) activeFromInputs.push('Al')
      if (inputModelData.value.aguaPorcentual <= 40) activeFromInputs.push('Sequía')

      const primary: StressKey = activeFromInputs[0] ?? 'Sin estrés'

      const combined = Array.from(
        new Set([primary, ...activeFromInputs].filter((stress) => stress !== 'Sin estrés'))
      ) as StressKey[]

      const base = stressMeta[primary] ?? stressMeta['Sin estrés']
      const stressLabel = combined.length > 0
        ? combined.map((stress) => stressMeta[stress].label).join(' + ')
        : stressMeta['Sin estrés'].label

      if (combined.length > 1) {
        return {
          stressKey: primary,
          stressLabel,
          tolerance: 'Media' as const,
          meaning: `Línea de cultivo resiliente ante ${stressLabel}, indicando un buen rendimiento en condiciones adversas.`,
        }
      }

      if (combined.length === 0) {
        return {
          stressKey: 'Sin estrés',
          stressLabel,
          tolerance: stressMeta['Sin estrés'].tolerance,
          meaning: 'Línea de cultivo resiliente en condiciones generales, indicando un buen rendimiento en condiciones adversas.',
        }
      }

      return {
        stressKey: primary,
        stressLabel,
        tolerance: base.tolerance,
        meaning: `Línea de cultivo resiliente ante ${stressLabel}, indicando un buen rendimiento en condiciones adversas.`,
      }
    })()

    result.value = {
      predicted_line: data.predicted_line,
      probabilities: data.probabilities,
      genes: data.genes.map((g: unknown) =>
        typeof g === 'string'
          ? g
          : isGeneObj(g)
            ? { gene: g.gene, score: g.score ?? 0, stresses: g.stresses ?? [] }
            : String(g)
      ),
      context: {
        cultivo: inputModelData.value.cultivo,
        ...stressInfo,
      },
    }
    emit('prediction-updated', result.value)
  } catch (err: unknown) {
    // Mostrar errores explícitos si vienen del backend
    // Axios errors tienen estructura err.response?.data?.detail
    if (err instanceof UnsupportedCropError) {
      errorMsg.value = `Modelo no disponible para ${err.cultivo}.`
    } else if (axios.isAxiosError(err)) {
      if (!err.response) {
        const base = api.defaults.baseURL || 'desconocida'
        errorMsg.value = `No se pudo conectar con el backend (${base}). Verifique que esté activo.`
      } else if (err.response?.data) {
      type BackendError = { detail?: unknown }
      const data = err.response.data as BackendError
      if (typeof data.detail === 'string') {
        errorMsg.value = data.detail
      } else {
        errorMsg.value = 'Error al obtener la predicción. Intente nuevamente más tarde.'
      }
      }
    } else {
      errorMsg.value = 'Error al obtener la predicción. Intente nuevamente más tarde.'
    }
    emit('prediction-updated', null)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.prediction-panel {
  background: linear-gradient(180deg, #f4f7ef 0%, #edf2e7 100%);
  border-radius: 16px;
  box-shadow: 0 18px 32px rgba(35, 52, 32, 0.12);
  border: 1px solid rgba(63, 90, 48, 0.2);
  height: 100%;
  overflow-y: auto;
}

.form-panel {
  background: linear-gradient(180deg, #f7faf3 0%, #eef3e7 100%);
}

.form-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(22, 32, 18, 0.08);
  box-shadow: 0 10px 20px rgba(18, 29, 16, 0.08);
}

.results-panel {
  background: linear-gradient(180deg, #f1f6ea 0%, #e7f0de 100%);
}

.results-title {
  font-family: "Playfair Display", "Times New Roman", serif;
  font-size: 22px;
  font-weight: 700;
  color: #2a3a28;
  text-align: center;
  letter-spacing: 0.3px;
}

.results-card {
  background: #ffffff;
  border: 1px solid rgba(22, 32, 18, 0.1);
  border-radius: 12px;
  min-height: 200px;
  box-shadow: 0 10px 20px rgba(18, 29, 16, 0.08);
}
</style>
