// store.js
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    query: {},
    // TODO: add query params
    results: [],
    show: false, // shows side panel
  },
  mutations: {
    setQuery(state, query) {
      state.query = query
    },
    setResults(state, results) {
      state.results = results
    },
    setShow(state, bool) {
      state.show = bool
    },
  },
  actions: {
    async search({ commit }, query) {
      commit('setQuery', query)

      const solrResponse = await axios.get('/solr/medications_core/select', {
        params: query,
      })

      commit('setResults', solrResponse.data.response.docs)
    },

    clearResults({ commit }) {
      commit('setResults', [])
    },

    showPanel({ commit }) {
      commit('setShow', true)
    },

    hidePanel({ commit }) {
      commit('setShow', false)
    },
  },

  getters: {
    query: (state) => state.query,
    results: (state) => state.results,
    show: (state) => state.show,
  },
})
