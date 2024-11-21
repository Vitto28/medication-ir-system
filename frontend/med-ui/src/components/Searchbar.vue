<script>
import axios from 'axios'

export default {
  data: () => ({
    loaded: false,
    loading: false,
    query: '',
    results: [],
  }),

  computed: {
    // TODO
    queryParams() {
      return {
        q: this.query || '*:*',
        wt: 'json',
      }
    },
  },

  methods: {
    async search() {
      this.loading = true

      // make query to solr
      const response = await axios.get('/solr/medications_core/select', {
        params: this.queryParams,
      })

      this.results = response.data.response.docs // get the array of results
      console.log(this.results)

      this.loading = false
      this.loaded = true
    },
  },
}
</script>

<template>
  <v-card class="mx-auto" color="surface-light" width="500px">
    <v-card-text>
      <v-text-field
        v-model="query"
        :loading="loading"
        append-inner-icon="mdi-magnify"
        density="compact"
        label="Search templates"
        variant="solo"
        hide-details
        single-line
        @click:append-inner="search"
      ></v-text-field>
    </v-card-text>
  </v-card>
  <v-container fluid>
    <v-textarea
      label="Label"
      v-model="query"
      name="input-7-1"
      variant="filled"
      auto-grow
      readonly
    ></v-textarea>
  </v-container>
  <div>
    <!-- for each element in the results, list them -->
    <v-list>
      <v-list-item v-for="result in results" :key="result.id">
        <v-list-item-content>
          <v-list-item-title>{{ result.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ result.id }}</v-list-item-subtitle>
          <v-list-tiem-subtitle>{{ result.description }}</v-list-tiem-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>
