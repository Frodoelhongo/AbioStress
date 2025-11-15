<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="header-custom">
      <q-toolbar style="background: #192e06; color: white; min-height: 70px; padding: 0 40px;">
        <q-tabs
          v-model="tab"
          class="nav-tabs"
          active-class="active-tab"
          indicator-color="transparent"
        >
          <q-tab
            v-for="link in navLinks"
            :key="link.id"
            :name="link.id"
            :label="link.label"
            class="nav-tab-item"
          />
        </q-tabs>
      </q-toolbar>
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
import { ref } from 'vue';

const navLinks = [
  { id: 'home', label: 'INICIO' },
  { id: 'database', label: 'BASE DE DATOS' },
  { id: 'gene-prediction', label: 'PREDICCIÓN DE LÍNEAS RESILIENTES' },
  { id: 'interpretation', label: 'INTERPRETACIÓN DE RESULTADOS' },
  { id: 'about-us', label: 'SOBRE NOSOTROS' }
];

const tab = ref('home');
</script>

<style scoped>
.header-custom {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.nav-tabs {
  flex: 1;
  max-width: 100%;
}

.nav-tab-item {
  color: white;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding: 0 20px;
  min-height: 70px;
  transition: background-color 0.3s ease;
}

.nav-tab-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.active-tab {
  background-color: rgba(255, 255, 255, 0.15);
  font-weight: 700;
}
</style>
