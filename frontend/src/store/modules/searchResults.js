const state = {
  searchItems: [],
  selectedCriteriaOption: null,
  selectedOrgOption: null,
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
  UPDATE_RESULTS ({ commit, state }) {
    // first filter out the 'noItem' item if it's present, because we don't want it in the full result list
    const filteredResults = state.searchItems.filter(document => {
      return document.type !== 'noresult_placeholder'
    })

    commit('SET_FORMATTED_ITEMS', filteredResults)
  }
}

const mutations = {
  SET_SEARCH (state, payload) {
    state.searchItems = payload
  },
  SET_SELECTED_ORG_OPTION (state, payload) {
    state.selectedOrgOption = payload
  },
  SET_SELECTED_CRITERIA_OPTION (state, payload) {
    state.selectedCriteriaOption = payload
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
  GET_FORMATTED_ITEMS: state => state.formattedItems,
  GET_SELECTED_ORG_OPTION: state => state.selectedOrgOption,
  GET_SELECTED_CRITERIA_OPTION: state => state.selectedCriteriaOption
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
