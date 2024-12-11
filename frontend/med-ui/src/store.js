// store.js
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    query: {},
    // TODO: add query params
    results: [],
    show: false, // shows side panel
    brands: {},
    formats: {},
    filters: '',
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
    setFacetBrands(state, brands) {
      state.brands = brands
    },
    setFacetFormats(state, formats) {
      state.formats = formats
    },
    setFilters(state, filters) {
      state.filters = filters
    },
  },
  actions: {
    async search({ commit }, qry) {
      // if (query != this.state.query) {
      //   commit('setQuery', query)
      // }

      const old_qry = qry.q

      if (this.state.filters) {
        qry.q = qry.q + ' ' + this.state.filters.filters
      }

      const solrResponse = await axios.get('/solr/medications_core/select', {
        params: qry,
      })

      qry.q = old_qry

      commit('setResults', solrResponse.data.response.docs)
    },

    async facetBrands({ commit }) {
      const solrResponse = await axios.get('/solr/medications_core/select', {
        params: {
          q: '*:*',
          rows: 0,
          facet: true,
          'facet.field': 'brand_names',
        },
      })

      const response = solrResponse.data.facet_counts.facet_fields.brand_names

      // turn array into object
      const brands = {}
      for (let i = 0; i < response.length; i += 2) {
        brands[response[i]] = response[i + 1]
      }

      commit('setFacetBrands', brands)
    },

    async facetFormats({ commit }) {
      const solrResponse = await axios.get('/solr/medications_core/select', {
        params: {
          q: '*:*',
          rows: 0,
          facet: true,
          'facet.field': 'formats',
        },
      })

      const response = solrResponse.data.facet_counts.facet_fields.formats

      // turn array into object
      const formats = {}
      for (let i = 0; i < response.length; i += 2) {
        formats[response[i]] = response[i + 1]
      }

      commit('setFacetFormats', formats)
    },

    addFilters({ commit }, filters) {
      commit('setFilters', filters)
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
    brands: (state) => state.brands,
    formats: (state) => state.formats,
  },
})
