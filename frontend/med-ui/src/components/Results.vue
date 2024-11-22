<template>
  <div id="results">
    <div id="table" class="pane">
      <v-data-table @click:row="handleRowClick" :headers="headers" :items="results"> </v-data-table>
    </div>
    <v-expand-x-transition>
      <v-card
        v-if="results.length > 0"
        v-show="show"
        id="info"
        class="mx-auto elevation-4 ml-6"
        width="600"
      >
        <div class="d-flex justify-space-between">
          <v-card-title>{{ results[selectedId].name }}</v-card-title>
          <v-btn size="x-small" class="mr-2 mt-2 bg-success" icon @click="show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-card-text>
          <p>{{ results[selectedId].description }}</p>
          <p>Some of the side effects include:</p>
          <ul class="ml-4">
            <li v-for="effect in results[selectedId].side_effects" :key="effect">
              {{ effect }}
            </li>
          </ul>
        </v-card-text>
      </v-card>
    </v-expand-x-transition>
  </div>
  <v-btn @click="show = true">open</v-btn>
  <v-btn @click="show = false">close</v-btn>
</template>

<script>
export default {
  data: () => ({
    selectedId: 2,
    show: false,
    // available headers: name, description, side effects, dosage, precautions
    headers: [
      { title: 'Name', key: 'name' },
      { title: 'Description', key: 'description' },
      { title: 'Side effects', key: 'side_effects' },
      { title: 'Dosage', key: 'dosage' },
      { title: 'Precautions', key: 'precautions' },
    ],
  }),
  computed: {
    results() {
      return this.$store.getters.results
    },
  },
  methods: {
    handleRowClick(row) {
      this.show = true
    },
  },
}
</script>

<style>
#results {
  display: grid;
  grid-template-columns: 1fr auto;
}
#table {
  width: 100%;
}
.v-data-table__tr:hover {
  cursor: pointer;
  background-color: hsla(160, 100%, 37%, 0.2);
}
#info {
  max-height: 100%;
}
</style>