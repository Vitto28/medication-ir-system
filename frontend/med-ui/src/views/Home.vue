<template>
  <!-- Homepage -->
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Homepage</h1>
        <p>Welcome to the homepage of our app.</p>
        <a href="#/search"><v-btn>Search</v-btn></a>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('clearResults')
  },
}
</script>

<style>
</style>
