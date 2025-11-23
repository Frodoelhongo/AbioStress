<template>
  <div class="db-container">
    <!-- Cuadro informativo -->
    <div class="db-info-box">
      <p class="db-info-text">
        Esta base de datos contiene los conjuntos de datos de RNA-seq utilizados para el desarrollo de nuestros modelos predictivos. Todos los datos son de acceso público y representan perfiles de expresión génica en diferentes especies de cultivo bajo condiciones de estrés abiótico.
      </p>
    </div>

    <!-- Tabla -->
    <q-table
      class="my-sticky-header-table"
      flat
      bordered
      :rows-per-page-options="[0]"
      hide-pagination
      :filter="filter"
      :rows="filteredRows"
      :columns="columns as any"
      row-key="name"
      no-data-label="No registros disponibles."
      no-results-label="No se encontraron registros coincidentes"
      style="background: rgba(255, 255, 255, 0.95); height: calc(100vh - 180px)"
      virtual-scroll
    >
      <template v-slot:top-left>
        <div class="q-gutter-sm">
          <template v-for="specie in species" :key="specie">
            <q-radio v-model="selectedSpecies" :val="specie" :label="speciesDisplayNames[specie] || specie" />
          </template>
        </div>
      </template>
      <template v-slot:top-right>
        <q-input outlined rounded dense debounce="300" v-model="filter" placeholder="Buscar">
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template v-slot:append>
            <q-btn flat icon="close" @click="filter = ''" color="negative" :disabled="!filter" />
          </template>
        </q-input>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { rows, columns } from 'src/services/data';
import { ref, computed } from 'vue';

const filter = ref('');

// Mapeo de nombres científicos a nombres comunes
const speciesDisplayNames: Record<string, string> = {
  'Zea Mays': 'Maíz',
  'Sorghum bicolor': 'Sorgo',
  'Gossypium hirsutum': 'Algodón',
  'Citrullus lanatus': 'Sandía',
  'Solanum lycopersicum': 'Tomate'
};

const species = rows.reduce((uniqueSpecies, thisSpecies) => {
  if (!uniqueSpecies.find((val) => thisSpecies.especie === val)) {
    uniqueSpecies.push(thisSpecies.especie);
  }
  return uniqueSpecies;
}, [] as string[]);

const selectedSpecies = ref(species[0] || '');
const filteredRows = computed(() => {
  if (!selectedSpecies.value) return rows;
  return rows.filter((row) => row.especie === selectedSpecies.value);
});
</script>
<style lang="sass">
.db-container
  padding: 20px

.db-info-box
  background: rgba(255, 255, 255, 0.75)
  border-radius: 20px
  padding: 20px 30px
  margin: 0 auto 20px
  max-width: 900px
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)
  backdrop-filter: blur(8px)

.db-info-text
  font-size: 16px
  font-weight: 400
  color: #000
  margin: 0
  line-height: 1.6
  text-align: center

.my-sticky-header-table
  /* height or max-height is important */
  height: calc(100vh - 180px)
  border-radius: 8px
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: #f8f4ef

  thead tr th
    position: sticky
    z-index: 1
    white-space: normal
    word-wrap: break-word
  thead tr:first-child th
    top: 0

  tbody td
    white-space: normal
    word-wrap: break-word
    max-width: 200px
    text-align: center
    vertical-align: middle

  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px

  /* prevent scrolling behind sticky top row on focus */
  tbody
    /* height of all previous header rows */
    scroll-margin-top: 48px
</style>
