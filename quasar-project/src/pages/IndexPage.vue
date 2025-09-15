<template>
  <!--q-page class="row items-center justify-evenly">
  </q-page-->
  <q-tab-panels v-model="selectedTab" animated swipeable style="background-color: transparent;">
    <q-tab-panel name="home">
      <!--q-page class="row items-center justify-evenly"></q-page-->
      <section id="home" class="content-section">
        <div class="row items-center">
          <div class="col text-center">
            <img :src="abioStressTwas" alt="Logo" style="height: 50vh;" />
          </div>
          <div class="col text-center">
            <p class="text-h2">Bienvenidos a AbioStress-TWAS!</p>
            <br/>
            <p>En este servidor, entrenamos un modelo de redes neuronales para predecir qué genes responden al estrés por salinidad, sequía, temperatura y metales pesados en los cultivos de <i>Zea mays, Sorghum bicolor, Solanum lycopersicum, Gossypium hirsutum  y Citrullus lanatus</i>.</p>
            <br/>
            <p>Hemos desarrollado AbioStress-TWAS con el objetivo de ayudar a los usuarios a explorar qué genes podrían contribuir a generar cultivos más resilientes, a partir de la integración de características ambientales y propiedades del suelo.</p>
          </div>
        </div>
      </section>
    </q-tab-panel>
    <q-tab-panel name="database">
      <db-table />
    </q-tab-panel>
    <q-tab-panel name="gene-prediction">
      <section id="gene-prediction" class="content-section">
        <div style="max-width: 800px; margin: auto;">
          <p class="text-h2">Predicción de Genes</p>
          <p>Próximamente podrás predecir qué genes responden a estrés abiótico en los cultivos de interés, ingresando las características ambientales y del suelo.</p>
          <p>Por ahora, puedes explorar la base de datos para ver los genes que ya hemos identificado como relacionados con la respuesta al estrés abiótico.</p>
        </div>
      </section>
    </q-tab-panel>
    <q-tab-panel name="about-us">
      <section id="about-us" class="content-section">
        <div style="max-width: 1000px; margin: auto;">
          <p class="text-h2">Autores</p>
          <div class="row">
            <div class="col text-center">
              <h4>Angela Martínez</h4>
            </div>
            <div class="col text-center">
              <h4>Frida Orozco</h4>
            </div>
            <div class="col text-center">
              <h4>Liliana Torres</h4>
            </div>
          </div>
          <p class="text-center">Somos estudiantes de la Licenciatura en Ingeniería Bioquímica en la Facultad de Ciencias Biológicas de la Universidad Autónoma de Coahuila. Actualmente formamos parte del Laboratorio de Biorremediación, dirigido por el Dr. Nagamani Balagurusamy.</p>
          <div class="row items-center">
            <div class="col text-center">
              <img :src="logosBiorem" alt="Logo" style="width:100%;" />
            </div>
            <div class="col text-center">
              <p>Biorem Lab, fundado en 2007 en la Facultad de Ciencias Biológicas de Torreón, Coahuila, México, se dedica a comprender las comunidades microbianas, sus procesos bioquímicos y sus interacciones en ecosistemas naturales, biodigestores y plantas.</p>
            </div>
            <div class="col text-center">
              <img :src="logoUadecFcb" alt="Logo" style="width:100%;" />
            </div>
          </div>
        </div>
      </section>
    </q-tab-panel>
  </q-tab-panels>
</template>

<script setup lang="ts">

import DbTable from 'src/components/DbTable.vue';
import abioStressTwas from 'src/assets/abio-stress-twas.png';
import logosBiorem from 'src/assets/logos-biorem.png';
import logoUadecFcb from 'src/assets/logo-uadec-fcb.png';

const selectedTab = defineModel();
</script>
