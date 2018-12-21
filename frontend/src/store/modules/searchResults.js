import Vue from 'vue'
import { SearchMultipleFields } from '@/api/SearchMultipleFields'
import { GetFilterSelectedOption } from '@/mixins/GetFilterSelectedOption'

const state = {
  searchItems: [],
  noItem: [
    {
      document: JSON.stringify({
        name: 'Ingen resultater matcher din søgning'
      })
    }
  ]
}

const actions = {
  SET_SEARCH (state) {
    let vm = this
    vm.searchItems = []

    SearchMultipleFields(state)
      .then(res => {
        let results = []
        res.forEach(result => {
          results = results.concat(result)
        })

        /**
         * If we are searching within a specific field, we need only to return results
         * where inputVal was within that specific field.
         */
        results = GetFilterSelectedOption.methods.getFilterSelectedOption(this.selectedOption, results)

        if (!results.length) {
          results = results.concat(state.noItem)
        }

        /**
         * We need to use Vue.set() to update the searchItems object,
         * because otherwise searchItems would no longer be reactive.
         */
        vm.$set(vm, 'searchItems', results)
      })
      .catch(() => {
        vm.$set(vm, 'searchItems', state.noItem)
      })
  }
}

const mutations = {
  SET_SEARCH (state) {
    Vue.set(state)
  }
}

const getters = {
  GET_SEARCH: (state) => (id) => state[id] || []
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
