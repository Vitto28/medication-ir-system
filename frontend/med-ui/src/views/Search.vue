<template>
  <v-container>
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
      <!-- Advanced search -->
      <v-col class="pt-0" cols="12">
        <div class="d-flex justify-space-between">
          <v-switch
            v-model="advanced"
            color="secondary"
            label="Advanced search"
            :hint="
              advanced
                ? 'Selecting multiple filters applies an AND logic, meaning only items matching all selected formats will be shown.'
                : ''
            "
            :persistent-hint="advanced"
          ></v-switch>
          <div class="d-flex align-center" v-if="advanced">
            <!-- Brands Menu -->
            <div class="ml-4">
              <!-- Dropdown Menu -->
              <v-menu v-model="brandsMenuOpen" :close-on-content-click="false" offset-y>
                <!-- Dropdown Button -->
                <template v-slot:activator="{ props }">
                  <v-btn color="secondary" v-bind="props"> Select Brands </v-btn>
                </template>
                <!-- Dropdown Content -->
                <v-card>
                  <v-list class="filter_menu">
                    <v-list-item v-for="(item, index) in brands" :key="index">
                      <v-checkbox
                        :label="item.label"
                        :indeterminate="item.state == null"
                        @click.prevent="toggleState(brands, index)"
                        :model-value="item.state"
                      >
                      </v-checkbox>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-menu>
            </div>
            <v-btn
              class="ml-2"
              color="red-darken-2"
              icon="mdi-delete"
              @click="brands.forEach((item) => (item.state = false))"
            ></v-btn>
            <!-- Formats Menu -->
            <div class="ml-8">
              <!-- Dropdown Menu -->
              <v-menu v-model="formatMenuOpen" :close-on-content-click="false" offset-y>
                <!-- Dropdown Button -->
                <template v-slot:activator="{ props }">
                  <v-btn color="secondary" v-bind="props"> Select Formats </v-btn>
                </template>
                <!-- Dropdown Content -->
                <v-card>
                  <v-list class="filter_menu">
                    <v-list-item v-for="(item, index) in formats" :key="index">
                      <v-checkbox
                        :label="item.label"
                        :indeterminate="item.state == null"
                        @click.prevent="toggleState(formats, index)"
                        :model-value="item.state"
                      >
                      </v-checkbox>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-menu>
            </div>
            <v-btn
              class="ml-2"
              color="red-darken-2"
              icon="mdi-delete"
              @click="formats.forEach((item) => (item.state = false))"
            ></v-btn>
            <!-- Remove ALL filters button -->
            <v-btn
              class="ml-8"
              color="red-darken-2"
              @click="
                brands.forEach((item) => (item.state = false)),
                  formats.forEach((item) => (item.state = false))
              "
              >clear all filters</v-btn
            >
          </div>
        </div>
      </v-col>
      <v-col cols="12">
        <Results />
      </v-col>
    </v-row>
    <!-- <div id="header">
    <a href="#/"> <v-btn>Home</v-btn></a>
    <Searchbar />
  </div> -->
  </v-container>

  <!-- <Results /> -->
</template>

<script>
export default {
  data: () => ({
    advanced: false,
    formatMenuOpen: false,
    formats: {},
    brandsMenuOpen: false,
    brands: {},
  }),
  async beforeMount() {
    await this.$store.dispatch('facetBrands')
    await this.$store.dispatch('facetFormats')

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
  },
  methods: {
    // cycles through the states of the checkboxes in the filter menus
    toggleState(collection, index) {
      const item = collection[index]
      console.log(item)
      if (item.state === false) {
        collection[index].state = true // Indeterminate to true (+)
      } else if (item.state === true) {
        collection[index].state = null // True to indetermiante (-)
      } else {
        collection[index].state = false // (ignore)
      }
    },
  },
  computed: {
    // returns a string containing the selected filters (brands and formats)
    // the collections (brands and formats) are iterated over
    // if collection[index].state is true, the filter is selected as '+collection[index].label'
    // if collection[index].state is null, the filter is selected as '-collection[index].label'
    // else, the filter is not selected
    // if no filters are selected, returns an empty string
    filters() {
      // if advanced search is not enabled, return an empty string
      if (!this.advanced) {
        return ''
      }

      // save the selected filters in a string
      let filters = ''
      for (let i = 0; i < this.brands.length; i++) {
        const str = `brand_names:"${this.brands[i].label}"` // <- note the quotes, this ensures the brand name is treated as a single term"`
        if (this.brands[i].state === true) {
          filters += `+${str} ` // <- note the space at the end
        } else if (this.brands[i].state === null) {
          filters += `-${str} `
        }
      }
      for (let i = 0; i < this.formats.length; i++) {
        const str = `formats:"${this.formats[i].label}""`
        if (this.formats[i].state === true) {
          filters += `+${str} `
        } else if (this.formats[i].state === null) {
          filters += `-${str} `
        }
      }
      return filters
    },
  },
  watch: {
    // when the filters change, update the search results
    filters: {
      handler: function (val) {
        this.$store.dispatch('addFilters', { filters: val })
      },
    },
  },
}
</script>

<script setup>
import Searchbar from '@/components/Searchbar.vue'
import Results from '@/components/Results.vue'
</script>

<style>
#header {
  display: flex;
  justify-content: space-between;
  align-items: top;
  padding: 1rem;
}
.filter_menu {
  max-width: 500px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.filter_menu .v-selection-control {
  min-height: 0px;
}
.filter_menu .v-input__details {
  display: none;
}
</style>
