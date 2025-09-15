<template>
  <q-layout view="lHh Lpr lFf">
    <q-header >
      <q-toolbar style="background: #c2d47c; color: #000">
        <!--q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" /-->

        <img :src="abioStressTwasLogo" alt="Logo" width="50" height="50" />
        <q-toolbar-title class="text-bold">AbioStress-TWAS</q-toolbar-title>
        <q-tabs
          v-model="tab"
          dense
          class="link"
          active-class="active-link"
          align="justify"
          narrow-indicator
        >
          <q-tab v-for="link in navLinks"
          :key="link.id"
          :name="link.id" :label="link.label" />
        </q-tabs>
      </q-toolbar>
      <hr style="border: 3px solid #5b672d; padding: 0; margin: 0;"/>
    </q-header>

    <!--q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer-->

    <q-page-container>
      <router-view v-model="tab" />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">

//import bioremLogo from 'src/assets/biorem-square.png';
import abioStressTwasLogo from 'src/assets/abio-stress-twas-logo.png';
import { ref } from 'vue';

const navLinks = [
  { id: 'home', label: 'INICIO' },
  { id: 'database', label: 'BASE DE DATOS' },
  { id: 'gene-prediction', label: 'PREDICCIÓN DE GENES' },
  { id: 'about-us', label: 'SOBRE NOSOTROS' }
];

const tab = ref('home');
</script>
<style scoped>
.active-link {
  font-weight: bold;
}
.link {
  color: #000;
  text-decoration: none;
  font-size: large;
}
</style>
