<script>
import Home from './views/Home.vue'
import Search from './views/Search.vue'

const routes = {
  '/': Home,
  '/search': Search,
}

export default {
  data() {
    return {
      currentPath: window.location.hash,
    }
  },
  computed: {
    currentView() {
      return routes[this.currentPath.slice(1) || '/'] || NotFound
    },
  },
  mounted() {
    window.addEventListener('hashchange', () => {
      this.currentPath = window.location.hash
    })
  },
}
</script>

<template>
  <component :is="currentView" />
</template>
