<template>
  <v-container>
    <v-row>
      <v-col class="d-flex flex-column align-center mt-16 mb-16" cols="12">
        <h1 class="text-h1 font-weight-medium">PharmaSeek</h1>
        <p class="text-subtitle-1">
          The number one place to find information about drugs and medications (citation needed).
        </p>
        <a class="mt-4" href="#/search"><v-btn class="bg-success">Star searching</v-btn></a>
      </v-col>
    </v-row>
    <v-row class="mb-14">
      <v-col class="d-flex flex-column align-center" cols="12">
        <h1 class="text-h4">What is this?</h1>
        <p class="w-66">
          This is a simple prototype of an information retrieval system for medications, allowing
          you to search for drugs by name, description, side effects, dosage, or precautions.
        </p>
      </v-col>
    </v-row>
    <!-- Features section (grid format, each feature has a title and a description): filtering, tabular format, automatic recomendation  -->
    <v-row class="mb-16">
      <v-col class="d-flex flex-column align-center" cols="12">
        <h1 class="text-h4 mb-5">Features</h1>
        <v-row>
          <v-col cols="4">
            <h2 class="text-h5">Filtering</h2>
            <p>Filter the results by name, description, side effects, dosage, or precautions.</p>
          </v-col>
          <v-col cols="4">
            <h2 class="text-h5">Tabular format</h2>
            <p>
              View the results in a tabular format, with the ability to sort and filter the data.
            </p>
          </v-col>
          <v-col cols="4">
            <h2 class="text-h5">Automatic recommendation</h2>
            <p>Get automatic recommendations based on your search query.</p>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <!-- credits: who this was created by (two people, give names), where the data was scraped from, and the used libraries/tools -->
    <v-row>
      <v-col class="d-flex flex-column align-center" cols="12">
        <h1 class="text-h4">Credits</h1>
        <p class="w-66">
          This project was created by <strong>Vittoria Scocco</strong> and
          <strong>Mehmet Bayazit</strong>. The data was scraped from
          <a href="https://example.com">example.com</a>. The project uses the following libraries
          and tools: Vue.js, Vuetify, Vuex, Axios, Apache Solr, and Scrapy/Beautiful Soup.
        </p>
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

<style scoped>
/* all text is centered */
p {
  text-align: center;
}

h1,
h2,
h3 {
  text-align: center;
}
</style>
