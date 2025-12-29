<template>

  <q-splitter v-model="splitterModel" style="height: calc(100vh - 100px)">
    <!-- Izquierda: formulario -->
    <template v-slot:before>
      <div class="q-pa-md" style="background: rgba(255, 255, 255, 0.95); border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); height: 100%; overflow-y: auto">
        <q-form class="q-gutter-md" @submit="submitForm">
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
          <q-input v-model.number="inputModelData.nacl" label="Concentración de NaCl (Ppm)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.cd" label="Concentración de Cd (Ppm)"
                   type="number" outlined dense required />
          <q-input v-model.number="inputModelData.al" label="Concentración de Al (Ppm)"
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
      <div class="q-pa-md" style="background: rgba(255, 255, 255, 0.95); border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); height: 100%; overflow-y: auto">
        <div class="row items-center justify-between q-mb-md">
          <div class="text-h5 text-center col-grow">Resultados de la Predicción</div>
        </div>

        <!-- Resultados de predicción -->

        <div class="q-mt-md">
            <div class="q-pa-md" style="background: rgba(255, 255, 255, 0.95); border: 1px solid #ccc; border-radius: 8px; min-height: 200px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)">
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
  } | null]
}>()

const splitterModel = ref(50)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const result = ref<null | {
  predicted_line: string
  probabilities: Record<string, number>
  genes: Array<{ gene: string; score: number; stresses: string[] } | string>
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
  temperatura:25,
  humedadRelativa: 56,
  intensidadLuminica: 2300,
  pH: 7.5,
  humedadSuelo: 24,
  carbonoOrganico: 0.2,
  nitrogenoTotal: 0.03,
  fosforoSoluble: 3.0,
  texturaSuelo: 'Arcilloso',
  aguaPorcentual: 10,
  nacl: 0,
  cd: 0,
  al: 0,
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
    }
    emit('prediction-updated', result.value)
  } catch (err: unknown) {
    // Mostrar errores explícitos si vienen del backend
    // Axios errors tienen estructura err.response?.data?.detail
    const anyErr = err as any
    if (err instanceof UnsupportedCropError) {
      errorMsg.value = `Modelo no disponible para ${err.cultivo}.`
    } else if (anyErr && anyErr.response && anyErr.response.data && anyErr.response.data.detail) {
      errorMsg.value = String(anyErr.response.data.detail)
    } else {
      errorMsg.value = 'Error al obtener la predicción. Intente nuevamente más tarde.'
    }
    emit('prediction-updated', null)
  } finally {
    loading.value = false
  }
}
</script>
