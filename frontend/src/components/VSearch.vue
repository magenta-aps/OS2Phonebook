<template>
  <b-nav-form>
    <v-autocomplete
      class="col"
      type="search"
      placeholder="Søg"
      :items="items"
      v-model="item"
      :get-label="getLabel"
      :component-item='template'
      @item-clicked="selected(item)"
      @update-items="updateItems"
      :auto-select-one-item="false"
      :min-len="2"
    />

    <b-button class="col-2 bg-primary" type="submit" v-on:click.prevent="viewSearchResults">
      <icon name="search"/>
    </b-button>
  </b-nav-form>
</template>

<script>
import Search from '@/api/Search'
import VSearchBarTemplate from './VSearchBarTemplate'
import VAutocomplete from 'v-autocomplete'
import '../../node_modules/v-autocomplete/dist/v-autocomplete.css'

export default {
  name: 'Search',

  components: {
    VAutocomplete
  },

  data () {
    return {
    /**
     * The item, items, routeName component value.
     * Used to detect changes and restore the value.
     */
      item: null,
      items: [],
      template: VSearchBarTemplate,
      /**
       * The noItem component value.
       * Used to give a default name.
       */
      noItem: [{ name: 'Ingen resultater matcher din søgning' }]
    }
  },

  methods: {
    /**
     * Get label name.
     */
    getLabel (item) {
      return item ? item.name : null
    },

    /**
     * Update employee or organisation suggestions based on search query.
     */
    updateItems (inputVal) {
      let vm = this
      vm.items = []

      Search.employees('name', inputVal)
        .then(response => {
          let searchResults = response.response.docs.length > 0 ? response.response.docs : vm.noItem
          // We need to use Vue.set() to update the items object, because otherwise items would no longer be reactive.
          // We update items with the original array + the new search results concatenated onto it.
          vm.$set(vm, 'items', vm.items.concat(searchResults))
        })
      Search.departments('name', inputVal)
        .then(response => {
          let searchResults = response.response.docs.length > 0 ? response.response.docs : vm.noItem
          vm.$set(vm, 'items', vm.items.concat(searchResults))
        })
    },

    /**
     * Go to the selected route.
     */
    selected (searchResult) {
      if (this.item.parent) {
        this.$router.push({ name: 'organisation', params: { result: searchResult } })
      }
      if (!this.item.parent) {
        this.$router.push({ name: 'person', params: { uuid: searchResult.uuid } })
      }
    },

    /**
     * View all search results for the given search string
     */
    viewSearchResults () {
      this.$router.push({ name: 'result', params: { results: this.items } })
    }
  }
}
</script>
