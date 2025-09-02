<template>
  <q-layout view="lHh Lpr lFf">
    <q-header >
      <q-toolbar style="background: #c2d47c; color: #000">
        <!--q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" /-->

        <img :src="abioStressTwasLogo" alt="Logo" width="50" height="50" />
        <q-toolbar-title class="text-bold">AbioStress-TWAS</q-toolbar-title>

        <q-item
          v-for="link in navLinks"
          :key="link.id"
          clickable
          v-ripple

          :class="{ 'active-link': activeSection === link.id }"
        >
      <q-item-section>
        <a class = 'link' :href="'#' + link.id">{{ link.label }}</a>
      </q-item-section>
    </q-item>
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
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">

//import bioremLogo from 'src/assets/biorem-square.png';
import abioStressTwasLogo from 'src/assets/abio-stress-twas-logo.png';
import { ref } from 'vue';

const activeSection = ref('home');
const navLinks = [
  { id: 'home', label: 'INICIO' },
  { id: 'database', label: 'BASE DE DATOS' },
  { id: 'about-us', label: 'SOBRE NOSOTROS' }
];

// find id of the section the page is in
import { onMounted, onBeforeUnmount } from 'vue';

function getCurrentSectionId() {
  const scrollPosition = window.scrollY + 100; // offset for header
  for (const link of navLinks) {
    const section = document.getElementById(link.id);
    if (section) {
      const top = section.offsetTop;
      const bottom = top + section.offsetHeight;
      if (scrollPosition >= top && scrollPosition < bottom) {
        return link.id;
      }
    }
  }
  return navLinks?.[0]?.id || '';
}

function handleScroll() {
  activeSection.value = getCurrentSectionId();
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  handleScroll();
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
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
