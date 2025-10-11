<template>
  <div class="text-h4 text-center q-pa-md">Predicción de Genes</div>
  <q-splitter v-model="splitterModel" style="height: calc(100vh - 200px)">
    <template v-slot:before>
      <div class="q-pa-md">
        <q-form class="q-gutter-md" @submit="submitForm">
          <q-select
            v-model="inputModelData.cultivo"
            label="Cultivo"
            :options="['Maíz', 'Sorgo', 'Tomate', 'Algodón', 'Sandía']"
            outlined
            dense
            required
          />
          <p class="text-bold">Condiciones ambientales</p>
          <q-input
            v-model.number="inputModelData.temperatura"
            label="Temperatura (°C)"
            type="number"
            outlined
            dense
            required
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
          <q-btn label="Predecir" color="primary" class="full-width" type="submit" />
        </q-form>
      </div>
    </template>

    <template v-slot:after>
      <div class="q-pa-md">
        <div class="text-h5 text-center q-mb-md">Resultados de la Predicción</div>
        <div class="q-pa-md" style="border: 1px solid #ccc; border-radius: 8px; min-height: 200px">
          <!-- Aquí se mostrarán los resultados de la predicción -->
          <p class="text-center text-grey">Los resultados aparecerán aquí.</p>
        </div>
      </div>
    </template>
  </q-splitter>
</template>
<script setup lang="ts">
import { ref } from 'vue';

import type { GENE_MODEL_INPUTS } from 'src/services/gene-model';

const inputModelData = ref<GENE_MODEL_INPUTS>({
  cultivo: 'Maíz',
  temperatura: 25,
  humedadRelativa: 60,
  intensidadLuminica: 800,
  pH: 6.5,
  humedadSuelo: 40,
  carbonoOrganico: 2.5,
  nitrogenoTotal: 0.15,
  fosforoSoluble: 15,
  texturaSuelo: 'Franco',
  aguaPorcentual: 20,
  nacl: 0.1,
  cd: 0.05,
  al: 0.02,
});

const splitterModel = ref(50);

const submitForm = () => {
  // in development alert
  alert('Funcionalidad en desarrollo');
};
</script>
