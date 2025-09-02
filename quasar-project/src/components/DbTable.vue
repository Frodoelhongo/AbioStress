<template>
  <q-table
    flat bordered
    :rows-per-page-options="[0]"
    hide-pagination
    :filter="filter"
    :rows="rows"
    :columns="columns as any"
    row-key="name"
    no-data-label="No registros disponibles."
    no-results-label="No se encontraron registros coincidentes"
    style="background:transparent"
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
