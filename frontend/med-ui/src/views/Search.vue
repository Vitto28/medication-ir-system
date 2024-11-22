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
export default {}
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
</style>
