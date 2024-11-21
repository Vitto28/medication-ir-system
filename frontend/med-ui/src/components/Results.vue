<template>
  <v-btn @click="show = !show">Toggle info</v-btn>
  <div id="results">
    <div id="table" class="pane">
      <v-list v-show="results.length > 0">
        <v-list-item v-for="result in results" :key="result.id">
          <v-list-item-title>{{ result.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ result.description }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </div>
    <div v-if="show" id="info" class="pane">Hello</div>
  </div>
</template>

<script>
export default {
  data: () => ({
    selected: null,
    show: false,
  }),
  computed: {
    results() {
      return this.$store.getters.results
    },
  },
}
</script>

<style>
#results {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
</style>