<template>
  <div class="d-flex flex-column align-center">
    <div class="d-flex flex-column align-center" v-if="results.length == 0" id="no_results">
      <v-sheet width="800" class="mt-16 d-flex flex-column" v-if="!this.firstSearchPerformed">
        <p class="text-h2 font mb-4">Welcome to PharmaSeek!</p>
        <h2 class="text-h5">Your trusted tool for medication information</h2>
        <p>Easily search, explore, and learn about medications with our intuitive platform. PharmaSeek provides reliable
          and detailed information on medications to help you make informed decisions.</p>
        <h2 class="text-h5 mt-8">What PharmaSeek provides</h2>
        <!-- numbered list -->
        <ol class="ml-6 mt-2">
          <li class="text-h6">Search for medications</li>
          <p>Use the search bar above to find specific medications by name, description, or related terms. The results
            will be neatly displayed in a tabular format that allows you to quickly scan and identify relevant
            medications.</p>
          <li class="text-h6">Refine your search</li>
          <p>Use the filters menu on the right to narrow down your search results based on specific criteria such as
            brand name, drug format, and drug class. This will help you find the most relevant medications for your
            needs.</p>
          <li class="text-h6">Explore related medications and their uses.</li>
          <p>Click on a medication to view detailed information about its uses, side effects, storage conditions, and
            more. Furthermore, we will automatically suggest related medications that you may find useful.</p>
        </ol>

        <h2 class="text-h5 mt-8">Disclaimer</h2>
        <p>The data provided on this platform is for educational purposes and should not replace professional medical
          advice, diagnosis, or treatment. Always consult a licensed healthcare provider for specific medical concerns
          or before starting any new medication.</p>
      </v-sheet>
      <div class="mt-16 d-flex flex-column align-center" v-else>
        <p class="text-h2 font mb-4">No results found</p>
        <p>Sorry, we couldn't find any medications matching your search :(</p>
        <p>Try adjusting the keywords in your query or the filters you set and try again</p>
      </div>

      <!-- Sorry, search returned no results -->
    </div>
    <div v-else id="results">
      <div id="table">
        <v-data-table :headers="headers" :items="results" item-value="id">
          <template v-slot:body="{ items }">
            <tr class="row" v-for="item in items" :key="item.id" @click="handleRowClick(item.id)">
              <td>{{ item.name }}</td>
              <td class="clas textwrap">{{ item.classes && item.classes.length > 0 ? item.classes.join(', ') : 'None' }}
              </td>
              <td class="description textwrap">{{ item.prescription }}</td>
              <td class="formats textwrap">{{ item.formats.join(', ') }}</td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- Popup panel with medications info -->
      <v-dialog max-width="1200">
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn id="open_btn" v-bind="activatorProps" color="surface-variant" text="Open Dialog" variant="flat"
            transition="dialog-bottom-transition"></v-btn>
        </template>

        <template v-slot:default="{ isActive }">
          <v-card v-if="results.length > 0" v-show="showPanel" id="info" class="mx-auto elevation-4 ml-6">
            <div class="d-flex justify-space-between">
              <v-card-title class="text-h4 panel_title">{{ selectedData.name }}</v-card-title>
              <v-btn size="x-small" class="mr-2 mt-2 bg-secondary" icon @click="isActive.value = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
            <!-- TODO: Move to its own component -->
            <v-card-text class="panel pt-0">
              <div class="mb-4">
                <!-- Brand names -->
                <div>
                  <p class="font-weight-bold">Brand names</p>
                  <!-- if brand names array is empty, do  -->
                  <p class="mb-5" v-if="selectedData.brand_names == null">
                    No brand names available.
                  </p>
                  <div v-else>
                    <v-chip v-for="format in selectedData.brand_names" :key="format" class="mr-2 mb-5" color="secondary"
                      label>
                      {{ format }}
                    </v-chip>
                  </div>
                </div>

                <!-- Class -->
                <div v-if="selectedData.classes && selectedData.classes.length > 0">
                  <p class="font-weight-bold">Classes:</p>
                  <v-chip v-for="clas in selectedData.classes" :key="clas" class="mr-2 mb-2" color="secondary" label>
                    {{ clas }}
                  </v-chip>
                </div>
                <div v-else>
                  <p>No information available on drug classes.</p>
                </div>

                <!-- Formats -->
                <div class="mt-5" v-if="selectedData.formats.length > 0">
                  <p>Can be administered via</p>
                  <v-chip v-for="format in selectedData.formats" :key="format" class="mr-2 mb-2" color="secondary"
                    label>
                    {{ format }}
                  </v-chip>
                </div>
                <div v-else>
                  <p>No information available on formats</p>
                </div>

              </div>

              <!-- <div v-for="section in Objec" :key="section">
                <p>{{ field }}</p>
              </div> -->

              <div class="mb-4" v-for="section in panelSections" :key="section.field">
                <p class="text-h5">{{ section.title }}</p>
                <!-- data is available -->
                <div v-if="selectedData[section.field]">
                  <!-- side effects -->
                  <div v-if="section.field == 'side_effects'">
                    <p>Some of the side effects of taking {{ selectedData.name }} include:</p>
                    <ul class="ml-4 mt-1">
                      <li v-for="effect in selectedData.side_effects" :key="effect">
                        {{ effect }}
                      </li>
                    </ul>
                  </div>
                  <!-- precautions -->
                  <div v-else-if="section.field == 'precautions'">
                    <ul class="ml-4 mt-1">
                      <li v-for="prec in selectedData.precautions" :key="prec">
                        {{ prec }}
                      </li>
                    </ul>
                  </div>
                  <div v-else>
                    <p>{{ selectedData[section.field] }} </p>
                  </div>
                </div>
                <!-- data aint available -->
                <div v-else>
                  <p>{{ section.empty }}</p>
                </div>
              </div>

              <!-- Related drugs -->
              <!-- Grid with three columns -->
              <!-- v-for card with title and short description -->
              <div class="mt-8">
                <p class="text-h5 mb-4">Related medications</p>
                <v-row>
                  <!-- v-for relatedDrugs array -->
                  <v-col cols="4" v-for="drug in relatedDrugs" :key="drug.id">
                    <v-card @click="openRelatedDrug(drug.id)" max-width="350"
                      style="overflow: hidden; white-space: normal; text-overflow: ellipsis;" hover rounded
                      class="textwra" :title="drug.name" :text="(drug.prescription).slice(0, 150) + '...'">
                      <!-- <v-card-title>{{ drug.name }}</v-card-title> -->
                      <!-- <v-card-text class="textwrap h-100">{{ drug.prescription }}</v-card-text> -->
                    </v-card>
                  </v-col>
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
    selectedData: {}, // stores the data from the selected item, as fetched from the API
    firstSearchPerformed: false,
    // defined the sections and their order in the extended-info panel
    panelSections: [
      {
        field: 'prescription',
        title: 'What it does',
        empty: 'No information available on what this medication does.'
      },
      {
        field: 'dosage',
        title: 'How to take',
        empty: 'No information available on how to take this medication.'
      },
      {
        field: 'side_effects',
        title: 'Side effects',
        empty: 'No information available on side effects.'
      },
      {
        field: 'storage',
        title: 'How to store',
        empty: 'No information available on how to store this medication.'
      },
      {
        field: 'missdose',
        title: 'What if I miss a dose?',
        empty: 'No information available on missing a dose.'
      },
      {
        field: 'overdose',
        title: 'Overdosing',
        empty: 'No information available on overdosing.'
      },
      {
        field: 'precautions',
        title: 'Precautions',
        empty: 'No information available on precautions.'
      },
    ],
    // TODO: Remove
    relatedDrugs: [],
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
    showPanel() {
      return this.$store.getters.show
    },
  },
  methods: {
    async fetchDrugData(id) {
      // fetch full data of the selected item
      this.selectedData = await this.$store.dispatch('fetchItem', id)
      // fetch related drugs
      this.relatedDrugs = await this.$store.dispatch('getRelatedDrugs', id)
    },
    async handleRowClick(id) {
      console.log('clicked row with id', id)
      await this.fetchDrugData(id)
      // grab button with id 'open_btn' and click it
      document.getElementById('open_btn').click()
      this.$store.dispatch('showPanel')
    },
    async openRelatedDrug(id) {
      await this.fetchDrugData(id)
      // scroll to the top
      document.getElementById('info').scrollTop = 0

    }
  },
  watch: {
    results() {
      if (this.firstSearchPerformed === false) {
        this.firstSearchPerformed = true
      }
    },
  },
}
</script>

<style>
.row:hover {
  cursor: pointer;
  background-color: hsla(160, 100%, 37%, 0.2);
}

.textwrap {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.description {
  max-width: 700px;
}

.clas {
  max-width: 200px;
}

.formats {
  max-width: 200px;
}

.panel {
  font-size: 1.1em;
}

.panel_title {
  white-space: wrap;
}

/* dont display item with id open_btn */
#open_btn {
  display: none;
}
</style>
