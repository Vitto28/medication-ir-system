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

      // use store to make the request
      this.$store.dispatch('search', this.query)

      this.loading = false
    },
  },
}
</script>

<template>
  <v-text-field
    v-model="queryString"
    :loading="loading"
    append-inner-icon="mdi-magnify"
    density="compact"
    label="Search templates"
    hint="For example, 'aspirin' or 'headache and fever'"
    single-line
    @click:append-inner="search"
    @keyup.enter="search"
  ></v-text-field>
</template>

<style scoped>
.v-text-field {
  min-width: 800px;
}
</style>