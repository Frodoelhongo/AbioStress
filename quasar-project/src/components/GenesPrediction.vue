<template>
  <div class="text-h4 text-center q-pa-md">Predicción de Genes</div>

  <q-splitter v-model="splitterModel" style="height: calc(100vh - 200px)">
    <!-- Izquierda: formulario -->
    <template v-slot:before>
      <div class="q-pa-md">
        <q-form class="q-gutter-md" @submit="submitForm">
          <!-- Crop selection -->
          <q-select
            v-model="inputModelData.cultivo"
            label="Cultivo"
            :options="['Maíz', 'Sorgo', 'Tomate', 'Algodón', 'Sandía']"
            outlined
            dense
            required
          />

          <!-- Warning in case that the model dont have the crop -->
          <q-banner
            v-if="inputModelData.cultivo !== 'Sandía'"
            class="bg-amber-2 text-amber-10 q-mt-sm"
            dense
          >
            Por ahora solo está disponible el modelo para <b>Sandía</b>.
          </q-banner>

          <p class="text-bold q-mt-md">Condiciones ambientales</p>
          <q-input
            v-model.number="inputModelData.temperatura"
            label="Temperatura (°C)"
            type="number"
            outlined
            dense
            required
            :rules="[num(-10, 50)]"
          />
          <q-input
            v-model.number="inputModelData.humedadRelativa"
            label="Humedad Relativa (%)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.intensidadLuminica"
            label="Intensidad Lumínica (µmol m⁻² s⁻¹)"
            type="number"
            outlined
            dense
            required
          />

          <p class="text-bold">Propiedades fisicoquímicas del suelo</p>
          <q-input
            v-model.number="inputModelData.pH"
            label="pH del Suelo"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.humedadSuelo"
            label="Humedad del Suelo (%)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.carbonoOrganico"
            label="Carbono Orgánico (%)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.nitrogenoTotal"
            label="Nitrógeno Total (%)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.fosforoSoluble"
            label="Fósforo Soluble (mg/kg)"
            type="number"
            outlined
            dense
            required
          />
          <q-select
            v-model="inputModelData.texturaSuelo"
            label="Textura del Suelo"
            :options="['Arenoso', 'Franco Arenoso', 'Franco', 'Franco Arcilloso', 'Arcilloso']"
            outlined
            dense
            required
          />

          <p class="text-bold">Condiciones de estrés abiótico</p>
          <q-input
            v-model.number="inputModelData.aguaPorcentual"
            label="Agua Porcentual (%)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.nacl"
            label="Concentración de NaCl (M)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.cd"
            label="Concentración de Cd (M)"
            type="number"
            outlined
            dense
            required
          />
          <q-input
            v-model.number="inputModelData.al"
            label="Concentración de Al (M)"
            type="number"
            outlined
            dense
            required
          />

          <q-btn
            label="Predecir"
            color="primary"
            class="full-width"
            type="submit"
            :disable="inputModelData.cultivo !== 'Sandía' || loading"
            :loading="loading"
          />
        </q-form>
      </div>
    </template>
    <!-- Derecha results -->
    <template v-slot:after>
      <div class="q-pa-md">
        <div class="text-h5 text-center q-mb-md">Resultados de la Predicción</div>

        <div class="q-pa-md" style="border: 1px solid #ccc; border-radius: 8px; min-height: 200px">
          <template v-if="errorMsg">
            <q-banner class="bg-red-2 text-red-10" dense>
              {{ errorMsg }}
            </q-banner>
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
                  :value="p"
                  color="primary"
                  track-color="grey-3"
                  size="10px"
                  rounded
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
                        <span
                          v-if="typeof g !== 'string' && g.score !== undefined"
                          class="text-grey-7"
                          >score: {{ g.score.toFixed(4) }}</span
                        >
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
    </template>
  </q-splitter>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import {
  predictGenes,
  UnsupportedCropError,
  type GENE_MODEL_INPUTS,
} from 'src/services/gene-model';

const splitterModel = ref(50);
const loading = ref(false);
const errorMsg = ref<string | null>(null);
const result = ref<null | {
  predicted_line: string;
  probabilities: Record<string, number>;
  genes: Array<{ gene: string; score: number; stresses: string[] } | string>;
}>(null);

// Valores por defecto del formulario
const inputModelData = ref<GENE_MODEL_INPUTS>({
  cultivo: 'Sandía',
  temperatura: undefined as unknown as number,
  humedadRelativa: undefined as unknown as number,
  intensidadLuminica: undefined as unknown as number,
  pH: undefined as unknown as number,
  humedadSuelo: undefined as unknown as number,
  carbonoOrganico: undefined as unknown as number,
  nitrogenoTotal: undefined as unknown as number,
  fosforoSoluble: undefined as unknown as number,
  texturaSuelo: undefined as unknown as
    | 'Arenoso'
    | 'Franco Arenoso'
    | 'Franco'
    | 'Franco Arcilloso'
    | 'Arcilloso',
  aguaPorcentual: undefined as unknown as number,
  nacl: undefined as unknown as number,
  cd: undefined as unknown as number,
  al: undefined as unknown as number,
});

const num =
  (min: number | null, max: number | null, msg = 'Fuera de rango') =>
  (v: unknown) => {
    if (v === '' || v === undefined || v === null || isNaN(v as number)) return 'Número requerido';
    const x = Number(v);
    if (min !== null && x < min) return msg + ` (≥ ${min})`;
    if (max !== null && x > max) return msg + ` (≤ ${max})`;
    return true;
  };

// Acción al enviar el formulario
async function submitForm() {
  errorMsg.value = null;
  result.value = null;

  // Validación: solo Sandía permitida por ahora
  if (inputModelData.value.cultivo !== 'Sandía') {
    errorMsg.value = 'Por ahora solo está disponible el modelo para Sandía.';
    return;
  }

  try {
    loading.value = true;
    // Define a local type for gene objects returned by the service
    type GeneObj = { gene: string; score?: number; stresses?: string[] };

    // Type-guard to narrow unknown entries to GeneObj
    function isGeneObj(x: unknown): x is GeneObj {
      if (typeof x !== 'object' || x === null) return false;
      const r = x as Record<string, unknown>;
      return typeof r.gene === 'string';
    }

    const data = await predictGenes(inputModelData.value); // ← corregido
    // Normalize the service response to the component's expected type:
    // ensure each gene entry has a defined score and stresses array
    result.value = {
      predicted_line: data.predicted_line,
      probabilities: data.probabilities,
      genes: data.genes.map((g: unknown) =>
        typeof g === 'string'
          ? g
          : isGeneObj(g)
            ? {
                gene: g.gene,
                score: g.score ?? 0,
                stresses: g.stresses ?? [],
              }
            : // fallback for unexpected shapes: stringify to avoid runtime errors
              String(g),
      ),
    };
  } catch (err: unknown) {
    if (err instanceof UnsupportedCropError) {
      errorMsg.value = `Modelo no disponible para ${err.cultivo}.`;
    } else {
      errorMsg.value = 'Error al obtener la predicción. Intente nuevamente más tarde.';
    }
  } finally {
    loading.value = false;
  }
}
</script>
