import './assets/main.css'

import { createApp } from 'vue'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Store
import store from './store'

// Components
import App from './App.vue'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App).use(vuetify).use(store).mount('#app')

export default createVuetify({
  icons: {
    defaultSet: 'mdi', // This is already the default value - only for display purposes
  },
})
