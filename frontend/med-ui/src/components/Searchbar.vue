<template>
  <v-row class="d-flex flex-column">
    <v-text-field variant="solo-filled" clearable v-model="query" :loading="loading" append-icon="mdi-magnify"
      density="compact" label="Search for medications" hint="For example, 'aspirin' or 'headache and fever'" single-line
      @click:append="search" @keyup.enter="search"></v-text-field>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    query: '',
    loading: false,
  }),

  methods: {
    async search() {
      this.loading = true

      // use store to make the request
      this.$store.dispatch('search', this.query)

      this.loading = false
    },
  },
}
</script>

<style scoped></style>
