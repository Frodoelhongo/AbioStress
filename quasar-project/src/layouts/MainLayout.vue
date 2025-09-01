<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <!--q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" /-->

        <img :src="bioremLogo" alt="Logo" width="50" height="50" />
        <q-toolbar-title>AbioStress-TWAS</q-toolbar-title>

      </q-toolbar>
    </q-header>

    <!--q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer-->

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">

import bioremLogo from 'src/assets/biorem-square.png';

</script>
