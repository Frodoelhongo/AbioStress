<template>
  <section id="about-us" class="content-section">
    <div style="max-width: 1000px; margin: auto">
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
      <p class="text-center">
        Somos estudiantes de la Licenciatura en Ingeniería Bioquímica en la Facultad de Ciencias
        Biológicas de la Universidad Autónoma de Coahuila. Actualmente formamos parte del
        Laboratorio de Biorremediación, dirigido por el Dr. Nagamani Balagurusamy.
      </p>
      <div class="row items-center">
        <div class="col text-center">
          <img :src="logosBiorem" alt="Logo" style="width: 100%" />
        </div>
        <div class="col text-center">
          <p>
            Biorem Lab, fundado en 2007 en la Facultad de Ciencias Biológicas de Torreón, Coahuila,
            México, se dedica a comprender las comunidades microbianas, sus procesos bioquímicos y
            sus interacciones en ecosistemas naturales, biodigestores y plantas.
          </p>
        </div>
        <div class="col text-center">
          <img :src="logoUadecFcb" alt="Logo" style="width: 100%" />
        </div>
      </div>
    </div>
  </section>
</template>
<script setup lang="ts">
import logosBiorem from 'src/assets/logos-biorem.png';
import logoUadecFcb from 'src/assets/logo-uadec-fcb.png';
</script>
