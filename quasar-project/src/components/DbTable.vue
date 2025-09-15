<template>
  <q-table
  class="my-sticky-header-table"
    flat bordered
    :rows-per-page-options="[0]"
    hide-pagination
    :filter="filter"
    :rows="rows"
    :columns="columns as any"
    row-key="name"
    no-data-label="No registros disponibles."
    no-results-label="No se encontraron registros coincidentes"
    style="background:transparent; height: calc(100vh - 100px);"
    virtual-scroll
  >
  <template v-slot:top-right>
        <q-input outlined rounded dense debounce="300" v-model="filter" placeholder="Buscar">
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template  v-slot:append>
            <q-btn flat icon="close"  @click="filter = ''" color="negative" :disabled="!filter" />
          </template>
        </q-input>
      </template>
  </q-table>
</template>

<script setup lang="ts">
import { rows, columns } from 'src/services/data';
import { ref } from 'vue';

const filter = ref('');

</script>
<style lang="sass">
.my-sticky-header-table
  /* height or max-height is important */
  height: 310px

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: #f8f4ef

  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0

  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px

  /* prevent scrolling behind sticky top row on focus */
  tbody
    /* height of all previous header rows */
    scroll-margin-top: 48px
</style>
