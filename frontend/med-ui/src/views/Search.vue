<template>

  <v-container class="h-screen">
    <v-row class="mt-4">
      <h1 class="text-h2 font-weight-medium d-flex">Pharma <p class="text-secondary">Seek</p>
      </h1>
    </v-row>
    <v-row id="container" justify="center">
      <v-col>
        <div v-if="modeEnabled" class="d-flex align-center">
          <!-- Search focus -->
          <v-tabs v-model="mode">
            <v-tab value="0" text="General Search">
              <template v-slot:append>
                <v-tooltip location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props" icon="mdi-help-circle-outline"></v-icon>
                  </template>
                  Prioritizes results that contain query terms in the description.
                </v-tooltip>
              </template>
            </v-tab>
            <v-tab value="1" text="Prescription">
              <template v-slot:append>
                <v-tooltip location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props" icon="mdi-help-circle-outline"></v-icon>
                  </template>
                  Limits results to those with matching prescription information.
                </v-tooltip>
              </template>
            </v-tab>
            <v-tab value="2" text="Side Effects">
              <template v-slot:append>
                <v-tooltip location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props" icon="mdi-help-circle-outline"></v-icon>
                  </template>
                  Limits results to those whose listed side effects match the query.
                </v-tooltip>
              </template>
            </v-tab>
          </v-tabs>
        </div>
        <Searchbar class="pt-3" />
        <Results class="mt-6" />
      </v-col>
      <v-col class="ml-10" cols="3">
        <v-sheet elevation="4" rounded="lg" class="pa-6">
          <h4 class="text-h5 font-weight-bold mb-4">Limit your search</h4>

          <p class="mb-4">
            To <b class="text-secondary">include</b> a term in your search, click on it
            once. Click again to <b class="text-error">exclude</b> it. Click a third time to <b>ignore</b> it.
            <br><br>
            Once you
            have selected your desired filters, click the search button <b>again</b> to re-rerun your search.
            <br><br>
            Keep in
            mind
            that filtering uses an <b>AND</b> operator, so only results that match all selected filters will be shown.
          </p>
          <!-- Formats -->
          <div class="d-flex mb-2 mt-4 align-center">
            <h4 class="text-h6 font-weight-bold">Formats</h4>
            <!-- clear all -->
            <v-btn class="ml-2" prepend-icon="mdi-trash-can-outline" variant="text" @click="clearFilters(formats)">
              clear all
            </v-btn>
          </div>

          <v-container fluid class="pa-0">
            <v-combobox density="compact" v-model:search="formatSearch" :custom-filter="filter" :items="formats"
              label="Type or select a format name" variant="solo" multiple>
              <template v-slot:item="{ item, index }">
                <v-list-item @click.prevent="toggleState(formats, index)">
                  <v-chip
                    :color="item.raw.state === true ? 'secondary' : item.raw.state === null ? 'error' : 'grey lighten-1'"
                    :text="item.raw.label" label></v-chip>
                </v-list-item>
              </template>
            </v-combobox>
            <!-- List the included AND excluded formats -->
            <p v-if="filteredFormats.length > 0">Filtered formats are:</p>
            <p v-else>No filtered formats selected.</p>
            <v-container class="pa-0">
              <v-chip class="ma-1" v-for="(format, index) in filteredFormats" :key="index"
                :color="format.state === true ? 'secondary' : 'error'">{{
                  format.label
                }}</v-chip>
            </v-container>
          </v-container>
          <!-- end formats -->

          <!-- Brands -->
          <div class="d-flex mb-2 mt-4 align-center">
            <h4 class="text-h6 font-weight-bold">Brands</h4>
            <!-- clear all -->
            <v-btn class="ml-2" prepend-icon="mdi-trash-can-outline" variant="text" @click="clearFilters(brands)">
              clear all
            </v-btn>
          </div>

          <v-container fluid class="pa-0">
            <v-combobox density="compact" v-model:search="brandSearch" :custom-filter="filter" :items="brands"
              label="Type or select a brand name" variant="solo" multiple>
              <template v-slot:item="{ item, index }">
                <v-list-item @click.prevent="toggleState(brands, index)">
                  <v-chip
                    :color="item.raw.state === true ? 'secondary' : item.raw.state === null ? 'error' : 'grey lighten-1'"
                    :text="item.raw.label" label></v-chip>
                </v-list-item>
              </template>
            </v-combobox>
            <!-- List the included AND excluded brands -->
            <p v-if="filteredBrands.length > 0">Filtered brands are:</p>
            <p v-else>No filtered brands selected.</p>
            <v-container class="pa-0">
              <v-chip class="ma-1" v-for="(brand, index) in filteredBrands" :key="index"
                :color="brand.state === true ? 'secondary' : 'error'">{{
                  brand.label
                }}</v-chip>
            </v-container>
          </v-container>

          <!-- end brands -->

          <!-- Classes -->
          <div class="d-flex mb-2 mt-4 align-center">
            <h4 class="text-h6 font-weight-bold">Classes</h4>
            <!-- clear all -->
            <v-btn class="ml-2" prepend-icon="mdi-trash-can-outline" variant="text" @click="clearFilters(classes)">
              clear all
            </v-btn>
          </div>

          <v-container fluid class="pa-0">
            <v-combobox density="compact" v-model:search="classSearch" :custom-filter="filter" :items="classes"
              label="Type or select a class name" variant="solo" multiple>
              <template v-slot:item="{ item, index }">
                <v-list-item @click.prevent="toggleState(classes, index)">
                  <v-chip
                    :color="item.raw.state === true ? 'secondary' : item.raw.state === null ? 'error' : 'grey lighten-1'"
                    :text="item.raw.label" label></v-chip>
                </v-list-item>
              </template>
            </v-combobox>
            <!-- List the included AND excluded classes -->
            <p v-if="filteredClasses.length > 0">Filtered classes are:</p>
            <p v-else>No filtered classes selected.</p>
            <v-container class="pa-0">
              <v-chip class="ma-1" v-for="(clas, index) in filteredClasses" :key="index"
                :color="clas.state === true ? 'secondary' : 'error'">{{
                  clas.label
                }}</v-chip>
            </v-container>
          </v-container>

          <!-- end classes -->

        </v-sheet>
      </v-col>
    </v-row>
  </v-container>


  <v-container v-if="false">
    <v-row>
      <v-col class="d-flex justify-space-between align-center" cols="12">
        <div>
          <h1>Search</h1>
          <p>
            Enter a query below to search for medications. You can enter specific terms or keywords,
            or use the advanced filtering options to narrow down your search.
          </p>
        </div>
        <a href="#/"> <v-btn>back to homepage</v-btn></a>
      </v-col>
      <v-col class="d-flex" cols="12">
        <Searchbar />
      </v-col>
      <v-col cols="12">
        <Results />
      </v-col>
    </v-row>
  </v-container>

  <!-- <Results /> -->
</template>

<script>
export default {
  data: () => ({
    formats: [],
    brands: [],
    classes: [],
    mode: 0, // focus of the search (general (0), prescription (1), side effects (2))
    modeEnabled: false,
    brandSearch: null,
    formatSearch: null,
    classSearch: null,

  }),

  // get the brands, formats, and classes from the store
  async beforeMount() {
    await this.$store.dispatch('facetBrands')
    await this.$store.dispatch('facetFormats')
    await this.$store.dispatch('facetClasses')

    var formats = this.$store.getters.formats
    this.formats = Object.keys(formats).map((key) => ({
      label: key,
      count: formats[key],
      state: false,
    }))

    var brands = this.$store.getters.brands
    this.brands = Object.keys(brands).map((key) => ({
      label: key,
      count: brands[key],
      state: false,
    }))

    var classes = this.$store.getters.classes
    this.classes = Object.keys(classes).map((key) => ({
      label: key,
      count: classes[key],
      state: false,
    }))
  },
  methods: {
    // cycles through the states of the checkboxes in the filter menus
    toggleState(collection, index) {
      const item = collection[index]
      if (item.state === false) {
        collection[index].state = true // Indeterminate to true (+)
      } else if (item.state === true) {
        collection[index].state = null // True to indeterminate (-)
      } else {
        collection[index].state = false // (ignore)
      }
    },

    clearFilters(collection) {
      for (let i = 0; i < collection.length; i++) {
        collection[i].state = false
      }
    },

    // handling brand filtering
    filter(val, queryText, item) {
      const toLowerCaseString = val =>
        String(val != null ? val : '').toLowerCase()

      const query = toLowerCaseString(queryText)

      const availableOptions = this.brands.filter(x => !this.model.includes(x))
      const hasAnyMatch = availableOptions.some(
        x => toLowerCaseString(x.title).includes(query)
      )

      const text = toLowerCaseString(item.raw.label)

      return text.includes(query)
    },


  },
  computed: {
    // these two computed properties are used to display the selected filters
    filteredBrands() {
      // returns brands that have state == true or null
      return this.brands.filter(brand => brand.state === true || brand.state === null)
    },
    filteredClasses() {
      // returns classes that have state == true or null
      return this.classes.filter(clas => clas.state === true || clas.state === null)
    },
    filteredFormats() {
      return this.formats.filter(format => format.state === true || format.state === null)
    },
    filters() {
      // returns the filters that are selected
      return {
        brand_names: this.filteredBrands,
        class: this.filteredClasses,
        formats: this.filteredFormats,
      }
    }

  },
  watch: {
    // when the filters change, update the search results
    filters: {
      handler: function (val) {
        this.$store.dispatch('addFilters', { filters: val })
      },
    },
    mode: {
      handler: function (val) {
        this.$store.dispatch('setMode', { mode: val })
      },
    },

  },
}
</script>

<script setup>
import Searchbar from '@/components/Searchbar.vue'
import Results from '@/components/Results.vue'
</script>

<style></style>
