import Vue from 'vue'
import Vuex from 'vuex'
import searchResults from './modules/searchResults'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    searchResults: searchResults
  }
})
