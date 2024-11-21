// src/services/solrService.js
import axios from 'axios'

const solrUrl = 'http://localhost:8983/solr/medications_core/select?q='

export const solrQuery = async (query, coreName) => {
  try {
    const response = await axios.get(`/solr/${coreName}/select`, {
      params: {
        q: query, // Query string
        wt: 'json', // JSON response format
      },
    })
    return response.data.response.docs
  } catch (error) {
    console.error('Error fetching Solr results:', error)
    throw error // Re-throw the error for handling in the component
  }
}
