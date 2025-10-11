<template>
  <!--q-page class="row items-center justify-evenly">
  </q-page-->
  <q-tab-panels v-model="selectedTab" animated swipeable style="background-color: transparent">
    <q-tab-panel name="home">
      <!--q-page class="row items-center justify-evenly"></q-page-->
      <section id="home" class="content-section">
        <div class="row items-center">
          <div class="col text-center">
            <img :src="abioStressTwas" alt="Logo" style="height: 50vh" />
          </div>
          <div class="col text-center">
            <p class="text-h2">Bienvenidos a AbioStress-TWAS!</p>
            <br />
            <p>
              En este servidor, entrenamos un modelo de redes neuronales para predecir qué genes
              responden al estrés por salinidad, sequía, temperatura y metales pesados en los
              cultivos de
              <i
                >Zea mays, Sorghum bicolor, Solanum lycopersicum, Gossypium hirsutum y Citrullus
                lanatus</i
              >.
            </p>
            <br />
            <p>
              Hemos desarrollado AbioStress-TWAS con el objetivo de ayudar a los usuarios a explorar
              qué genes podrían contribuir a generar cultivos más resilientes, a partir de la
              integración de características ambientales y propiedades del suelo.
            </p>
          </div>
        </div>
      </section>
    </q-tab-panel>
    <q-tab-panel name="database">
      <db-table />
    </q-tab-panel>
    <q-tab-panel name="gene-prediction">
      <section id="gene-prediction">
        <genes-prediction />
      </section>
    </q-tab-panel>
    <q-tab-panel name="about-us">
      <about-us />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script setup lang="ts">
import DbTable from 'src/components/DbTable.vue';
import AboutUs from 'src/components/AboutUs.vue';
import GenesPrediction from 'src/components/GenesPrediction.vue';

import abioStressTwas from 'src/assets/abio-stress-twas.png';

const selectedTab = defineModel();
</script>
