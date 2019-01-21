import { SearchMultipleFields } from '@/api/SearchMultipleFields'
import GetFilterSelectedOption from '@/mixins/GetFilterSelectedOption'

const state = {
  searchItems: [],
  noItem: [
    {
      document: JSON.stringify({
        name: 'Ingen resultater matcher din søgning',
        type: 'noresult_placeholder'
      })
    }
  ],
  refresh: false,
  formattedItems: []
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
  },

  UPDATE_RESULTS ({ commit, state }) {
    var results = []

    // first filter out the 'noItem' item if it's present, because we don't want it in the full result list
    const filteredResults = state.searchItems.filter(item => {
      const document = JSON.parse(item.document)
      return document.type !== 'noresult_placeholder'
    })

    for (var item = 0; item < filteredResults.length; item++) {
      if (filteredResults[item].document) {
        results.push(JSON.parse(filteredResults[item].document))
      }
    }
    commit('SET_FORMATTED_ITEMS', results)
  }
}

const mutations = {
  SET_SEARCH (state, payload) {
    state.searchItems = payload
  },
  UPDATE_RESULTS (state, payload) {
    state.refresh = payload
  },
  SET_FORMATTED_ITEMS (state, payload) {
    state.formattedItems = payload
  }
}

const getters = {
  GET_ITEMS: state => state.searchItems,
  GET_FORMATTED_ITEMS: state => state.formattedItems
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
