<template>
  <div id="header">
    <a href="#/"> <v-btn>Home</v-btn></a>
    <Searchbar />
  </div>

  <Results />
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
