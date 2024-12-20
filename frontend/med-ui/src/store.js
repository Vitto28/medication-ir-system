// store.js
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    results: [],
    show: false, // shows side panel
    brands: {},
    formats: {},
    filters: [],
    mode: '0',
  },
  mutations: {
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
    setMode(state, mode) {
      state.mode = mode
    },
  },
  actions: {
    async search({ commit }, query) {
      // TODO: change query depending on mode
      // TODO Return only relevant info, full data only pulled when necessary

      const baseURL = '/solr/medications_core/select'

      // set query string
      var queryString = 'NORESULTS'
      if (this.state.filters.length > 0) {
        queryString = '*:*'
      }
      if (query.length > 0) {
        queryString = query
      }

      // set parameters
      var params = new URLSearchParams({
        q: queryString,
        rows: 99999,
        wt: 'json',
      })

      // add filters
      this.state.filters.forEach((entry) => params.append('fq', entry))

      // limit the queried fields
      const desiredFields = ['id', 'name', 'class', 'prescription', 'formats']
      desiredFields.forEach((entry) => params.append('fl', entry))

      // query Solr
      const solrResponse = await axios.get(baseURL, { params })

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

    async facetClasses({ commit }) {
      const solrResponse = await axios.get('/solr/medications_core/select', {
        params: {
          q: '*:*',
          rows: 0,
          facet: true,
          'facet.field': 'class',
        },
      })

      const response = solrResponse.data.facet_counts.facet_fields.classes

      // turn array into object
      const classes = {}
      for (let i = 0; i < response.length; i += 2) {
        classes[response[i]] = response[i + 1]
      }

      commit('setFacetClasses', classes)
    },

    // Searches for a specific item with a given ID
    async fetchItem({ commit }, id) {
      // fetch full item from Solr
      const baseURL = '/solr/medications_core/select'
      const params = new URLSearchParams({
        q: `id:${id}`,
        rows: 1,
        wt: 'json',
      })

      // query Solr
      const solrResponse = await axios.get(baseURL, { params })

      return solrResponse.data.response.docs[0]
    },

    showPanel({ commit }) {
      commit('setShow', true)
    },

    hidePanel({ commit }) {
      commit('setShow', false)
    },

    addFilters({ commit }, ft) {
      // produce a proper filter string
      var filterArray = []
      const allFilters = ft['filters']

      Object.keys(allFilters).forEach((field) => {
        const filters = allFilters[field]
        Object.entries(filters).forEach(([idx, item]) => {
          var entry = `${field}:${item.label}`
          if (item.state == null) {
            entry = '-' + entry
          }
          filterArray.push(entry)
        })
      })
      console.log(filterArray)
      commit('setFilters', filterArray)
    },

    setMode({ commit }, mode) {
      commit('setMode', mode)
    },
  },

  getters: {
    results: (state) => state.results,
    show: (state) => state.show,
    brands: (state) => state.brands,
    formats: (state) => state.formats,
  },
})
