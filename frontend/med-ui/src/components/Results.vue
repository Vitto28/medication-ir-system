<template>
  <div class="d-flex flex-column align-center">
    <div class="d-flex flex-column align-center" v-if="results.length == 0" id="no_results">
      <p class="text-h2 font">No results found</p>
      <p>Sorry, we couldn't find any medications matching your search :(</p>
      <p>Try adjusting the keywords in your query or the filters you set and try again</p>
      <!-- Sorry, search returned no results -->
    </div>
    <div v-else id="results">
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

      <!-- Popup panel with medications info -->
      <v-dialog max-width="1200">
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn
            id="open_btn"
            v-bind="activatorProps"
            color="surface-variant"
            text="Open Dialog"
            variant="flat"
            transition="dialog-bottom-transition"
          ></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
          <v-card
            v-if="results.length > 0"
            v-show="showPanel"
            id="info"
            class="mx-auto elevation-4 ml-6"
          >
            <div class="d-flex justify-space-between">
              <v-card-title class="text-h4 panel_title">{{ selectedResult.name }}</v-card-title>
              <v-btn
                size="x-small"
                class="mr-2 mt-2 bg-secondary"
                icon
                @click="isActive.value = false"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
            <!-- TODO: Move to its own component -->
            <v-card-text class="panel pt-0">
              <div>
                <!-- Brand names -->
                <div>
                  <p class="font-weight-bold">Brand names</p>
                  <!-- if brand names array is empty, do  -->
                  <p class="mb-5" v-if="selectedResult.brand_names == null">
                    No brand names available.
                  </p>
                  <div v-else>
                    <v-chip
                      v-for="format in selectedResult.brand_names"
                      :key="format"
                      class="mr-2 mb-5"
                      color="secondary"
                      label
                    >
                      {{ format }}
                    </v-chip>
                  </div>
                </div>

                <!-- Class -->
                <div class="d-flex">
                  <p class="font-weight-bold mr-1 mb-4">Class:</p>
                  <p>No class available</p>
                </div>

                <!-- Formats -->
                <p>Can be administered via</p>
                <p class="text-subtitle-2">
                  (Note: This is placeholder information, may not match what's given below)
                </p>

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
              <div class="mt-4">
                <p class="text-h5">What it does</p>
                <p class="mb-8">{{ selectedResult.prescription }}</p>
              </div>

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
                <p v-if="selectedResult.storage">{{ selectedResult.storage }}</p>
                <p v-else>There is no information available on how to store this medication.</p>
              </div>

              <!-- Missed dose -->
              <div class="mb-4">
                <p class="text-h5">What if I miss a dose?</p>
                <p v-if="selectedResult.missdose">{{ selectedResult.missdose }}</p>
                <p v-else>There is no information available on missing a dose.</p>
              </div>

              <!-- Overdose -->
              <div class="mb-4">
                <p class="text-h5">Overdosing</p>
                <p v-if="selectedResult.overdose">{{ selectedResult.overdose }}</p>
                <p v-else>There is no information available on overdosing.</p>
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

              <!-- Related drugs -->
              <!-- Grid with three columns -->
              <!-- v-for card with title and short description -->
              <div class="mt-8">
                <p class="text-h5 mb-4">Related medications</p>
                <v-row>
                  <!-- v-for relatedDrugs array -->
                  <v-col cols="4" v-for="drug in selectedRelatedDrugs" :key="drug.id">
                    <v-card elevation="4">
                      <v-card-title>{{ drug.name }}</v-card-title>
                      <v-card-text class="textwrap">{{ drug.description }}</v-card-text>
                    </v-card>
                  </v-col>
                  <!-- <v-col cols="4">
                    <v-card>
                      <v-card-title>Drug 1</v-card-title>
                      <v-card-text>Short description</v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="4">
                    <v-card>
                      <v-card-title>Drug 2</v-card-title>
                      <v-card-text>Short description</v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="4">
                    <v-card>
                      <v-card-title>Drug 3</v-card-title>
                      <v-card-text>Short description</v-card-text>
                    </v-card>
                  </v-col> -->
                </v-row>
              </div>
            </v-card-text>
          </v-card>
          <!-- end card -->
        </template>
      </v-dialog>
      <!-- End popup -->
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    selectedId: null,
    // TODO: Remove
    selectedRelatedDrugs: [],
    relatedDrugs: [
      {
        id: 1,
        name: 'Paracetamol',
        description: 'Paracetamol is used to treat mild to moderate pain and reduce fever.',
      },
      {
        id: 2,
        name: 'Ibuprofen',
        description:
          'Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) for pain, inflammation, and fever.',
      },
      {
        id: 3,
        name: 'Amoxicillin',
        description: 'Amoxicillin is an antibiotic used to treat various bacterial infections.',
      },
      {
        id: 4,
        name: 'Metformin',
        description:
          'Metformin is used to manage type 2 diabetes by improving blood sugar control.',
      },
      {
        id: 5,
        name: 'Atorvastatin',
        description:
          'Atorvastatin is used to lower cholesterol and reduce the risk of heart disease.',
      },
      {
        id: 6,
        name: 'Omeprazole',
        description:
          'Omeprazole is used to treat acid reflux and ulcers by reducing stomach acid production.',
      },
      {
        id: 7,
        name: 'Levothyroxine',
        description: 'Levothyroxine is used to treat hypothyroidism by replacing thyroid hormone.',
      },
      {
        id: 8,
        name: 'Cetirizine',
        description:
          'Cetirizine is an antihistamine used to relieve allergy symptoms such as runny nose and itching.',
      },
      {
        id: 9,
        name: 'Clopidogrel',
        description:
          'Clopidogrel is an antiplatelet medication used to prevent blood clots in heart disease and stroke.',
      },
      {
        id: 10,
        name: 'Amlodipine',
        description:
          'Amlodipine is used to treat high blood pressure and angina by relaxing blood vessels.',
      },
      {
        id: 11,
        name: 'Alprazolam',
        description:
          'Alprazolam is a benzodiazepine used to treat anxiety and panic disorders by calming the brain.',
      },
      {
        id: 12,
        name: 'Sertraline',
        description:
          'Sertraline is an antidepressant used to treat depression, anxiety, and obsessive-compulsive disorder.',
      },
    ],
    // available headers: name, description, side effects, dosage, precautions
    headers: [
      { title: 'Name', value: 'name' },
      { title: 'Class', value: 'class' },
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
    // brands() {
    //   return this.$store.getters.brands
    // },
    // formats() {
    //   return this.$store.getters.formats
    // },
  },
  methods: {
    handleRowClick(id) {
      this.selectedId = id
      // grab button with id 'open_btn' and click it
      // choose three random related drugs and set them to selectedRelatedDrugs
      this.selectedRelatedDrugs = this.relatedDrugs.sort(() => Math.random() - 0.5).slice(0, 3)
      document.getElementById('open_btn').click()
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
.panel_title {
  max-width: 550px;
  white-space: wrap;
}
/* dont display item with id open_btn */
#open_btn {
  display: none;
}
</style>
