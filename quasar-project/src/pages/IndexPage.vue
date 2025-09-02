<template>
  <!--q-page class="row items-center justify-evenly">
  </q-page-->
  <main>
    <section id="home" class="content-section">
        <div class="row">
          <div class="col text-center">
            <img :src="abioStressTwas" alt="Logo" style="height: 50vh;" />
          </div>
          <div class="col text-center">
            <h2>Bienvenidos a AbioStress-TWAS!</h2>
            <p>En este servidor, entrenamos un modelo de redes neuronales para predecir qué genes responden al estrés por salinidad, sequía, temperatura y metales pesados en los cultivos de Zea mays, Sorghum bicolor, Solanum lycopersicum, Gossypium hirsutum  y Citrullus lanatus.</p>
            <p>Hemos desarrollado AbioStress-TWAS con el objetivo de ayudar a los usuarios a explorar qué genes podrían contribuir a generar cultivos más resilientes, a partir de la integración de características ambientales y propiedades del suelo.</p>
          </div>
        </div>
    </section>

    <section id="database" class="content-section">
        <h2>Base de datos</h2>
        <db-table />
    </section>

    <section id="about-us" class="content-section">
      <div style="max-width: 800px; margin: auto;">
        <h2>Autores</h2>
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
        <div class="row">
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
  </main>
</template>

<script setup lang="ts">

import DbTable from 'src/components/DbTable.vue';
import abioStressTwas from 'src/assets/abio-stress-twas.png';
import logosBiorem from 'src/assets/logos-biorem.png';
import logoUadecFcb from 'src/assets/logo-uadec-fcb.png';

</script>
