<template>
  <div id="results">
    <div id="table" class="pane">
      <v-data-table :headers="headers" :items="results" item-value="id" dense>
        <template v-slot:body="{ items }">
          <tr class="row" v-for="item in items" :key="item.id" @click="handleRowClick(item.id)">
            <td>{{ item.name }}</td>
            <td>{{ 'None' }}</td>
            <td class="description">{{ item.prescription }}</td>
            <td>{{ item.formats.join(', ') }}</td>
          </tr>
        </template>
      </v-data-table>
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
          <v-card-title>{{ selectedResult.name }}</v-card-title>
          <v-btn size="x-small" class="mr-2 mt-2 bg-success" icon @click="show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-card-text>
          <p>{{ selectedResult.description }}</p>
          <p>Some of the side effects include:</p>
          <ul class="ml-4">
            <li v-for="effect in selectedResult.side_effects" :key="effect">
              {{ effect }}
            </li>
          </ul>
          <p>Dosage: {{ selectedResult.dosage }}</p>
          <p>Precautions: {{ selectedResult.precautions }}</p>
        </v-card-text>
      </v-card>
    </v-expand-x-transition>
  </div>
</template>

<script>
export default {
  data: () => ({
    selectedId: null,
    show: false,
    // available headers: name, description, side effects, dosage, precautions
    headers: [
      { title: 'Name', key: 'name' },
      { title: 'Class', key: 'class' },
      { title: 'Description', value: 'prescription' },
      { title: 'Formats', value: 'formats' },
    ],
  }),
  computed: {
    results() {
      return this.$store.getters.results
    },
    selectedResult() {
      return this.results.find((result) => result.id == this.selectedId) || {}
    },
  },
  methods: {
    handleRowClick(id) {
      this.selectedId = id
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
.row:hover {
  cursor: pointer;
  background-color: hsla(160, 100%, 37%, 0.2);
}
#info {
  max-height: 100%;
}
.row {
  height: 100px;
}
.description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 700px;
}
</style>
