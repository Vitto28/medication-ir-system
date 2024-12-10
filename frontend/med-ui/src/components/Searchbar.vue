<template>
  <v-row class="d-flex flex-column">
    <v-text-field
      v-model="queryString"
      :loading="loading"
      append-inner-icon="mdi-magnify"
      density="compact"
      label="Search for medications"
      hint="For example, 'aspirin' or 'headache and fever'"
      single-line
      @click:append-inner="search"
      @keyup.enter="search"
    ></v-text-field>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    queryString: '',
    loading: false,
  }),

  computed: {
    // TODO
    query() {
      return {
        q: this.queryString || '*:*',
        wt: 'json',
      }
    },
  },

  methods: {
    async search() {
      this.loading = true

      this.$store.dispatch('hidePanel')

      // use store to make the request
      this.$store.dispatch('search', this.query)

      this.loading = false
    },
  },
}
</script>

<style scoped></style>
