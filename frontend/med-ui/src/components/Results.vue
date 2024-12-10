<template>
  <div id="results">
    <div id="table" class="pane">
      <v-data-table :headers="headers" :items="results" item-value="id" dense>
        <template v-slot:body="{ items }">
          <tr class="row" v-for="item in items" :key="item.id" @click="handleRowClick(item.id)">
            <td>{{ item.name }}</td>
            <td>{{ 'None' }}</td>
            <td class="description textwrap">{{ item.prescription }}</td>
            <td class="formats textwrap">{{ item.formats.join(', ') }}</td>
          </tr>
        </template>
      </v-data-table>
    </div>
    <v-expand-x-transition>
      <v-card
        v-if="results.length > 0"
        v-show="showPanel"
        id="info"
        class="mx-auto elevation-4 ml-6"
      >
        <div class="d-flex justify-space-between">
          <v-card-title class="text-h4">{{ selectedResult.name }}</v-card-title>
          <v-btn
            size="x-small"
            class="mr-2 mt-2 bg-success"
            icon
            @click="$store.dispatch('hidePanel')"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <!-- TODO: Move to its own component -->
        <v-card-text class="panel pt-0">
          <div>
            <!-- Brand names -->
            <p class="font-weight-bold">Brand names</p>
            <v-chip
              v-for="format in selectedResult.brand_names"
              :key="format"
              class="mr-2 mb-5"
              color="secondary"
              label
            >
              {{ format }}
            </v-chip>

            <!-- Class -->
            <div class="d-flex">
              <p class="font-weight-bold mr-1 mb-4">Class:</p>
              <p>No class available</p>
            </div>

            <!-- Formats -->
            <p>Can be administered via</p>
            <v-chip
              v-for="format in selectedResult.formats"
              :key="format"
              class="mr-2 mb-2"
              color="secondary"
              label
            >
              {{ format }}
            </v-chip>
          </div>

          <!-- Description -->
          <p class="mb-8 mt-4">{{ selectedResult.prescription }}</p>

          <!-- How to take -->
          <div class="mb-4">
            <p class="text-h5">How to take</p>
            <p>{{ selectedResult.dosage }}</p>
          </div>

          <!-- Side effects -->
          <div class="mb-4">
            <p class="text-h5">Side effects</p>
            <p>Some of the side effects of taking {{ selectedResult.name }} include:</p>
            <ul class="ml-4 mt-1">
              <li v-for="effect in selectedResult.side_effects" :key="effect">
                {{ effect }}
              </li>
            </ul>
          </div>

          <!-- Storing -->
          <div class="mb-4">
            <p class="text-h5">How to store</p>
            <p>{{ selectedResult.storage }}</p>
          </div>

          <!-- Missed dose -->
          <div class="mb-4">
            <p class="text-h5">What if I miss a dose?</p>
            <p>{{ selectedResult.missdose }}</p>
          </div>

          <!-- Overdose -->
          <div class="mb-4">
            <p class="text-h5">Overdosing</p>
            <p>{{ selectedResult.overdose }}</p>
          </div>

          <!-- Precautions -->
          <div>
            <p class="text-h5">Precautions</p>
            <ul class="ml-4">
              <li v-for="precaution in selectedResult.precautions" :key="precaution">
                {{ precaution }}
              </li>
            </ul>
          </div>
        </v-card-text>
      </v-card>
    </v-expand-x-transition>
  </div>
</template>

<script>
export default {
  data: () => ({
    selectedId: null,
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
    showPanel() {
      return this.$store.getters.show
    },
  },
  methods: {
    handleRowClick(id) {
      this.selectedId = id
      this.$store.dispatch('showPanel')
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
  /* width: 100%; */
}
.row:hover {
  cursor: pointer;
  background-color: hsla(160, 100%, 37%, 0.2);
}
#info {
  max-height: 100%;
}
.row {
  /* height: 100px; */
}
.textwrap {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.description {
  max-width: 700px;
}
.formats {
  max-width: 200px;
}
.panel {
  font-size: 1.1em;
}
</style>
