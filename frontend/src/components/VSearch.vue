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
      @item-selected="$emit('input', $event)"
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
      routeName: '',
      template: VSearchBarTemplate,
      /**
       * The noItem component value.
       * Used to give a default name.
       */
      noItem: [{ name: ['Ingen resultater matcher din søgning'] }]
    }
  },

  watch: {
    /**
     * Whenever route change update.
     */
    '$route' (to) {
      this.getRouteName(to)
    }
  },

  created () {
    /**
     * Called synchronously after the instance is created.
     * Get route name.
     */
    this.getRouteName(this.$route)
  },

  methods: {
    /**
     * Get label name.
     */
    getLabel (item) {
      return item ? item.name : null
    },

    /**
     * Get to the route name.
     * So if we're viewing an employee, it goes to the employee detail.
     */
    getRouteName (route) {
      if (route.name.indexOf('organisation') > -1) {
        this.routeName = 'organisation'
      }
      if (route.name.indexOf('person') > -1) {
        this.routeName = 'person'
      }
    },

    /**
     * Update employee or organisation suggestions based on search query.
     */
    updateItems (query) {
      let vm = this
      vm.items = []

      Search.employees(query)
        .then(response => {
          let searchResults = response.response.docs.length > 0 ? response.response.docs : vm.noItem
          // We need to use Vue.set() to update the items object, because otherwise items would no longer be reactive.
          // We update items with the original array + the new search results concatenated onto it.
          vm.$set(vm, 'items', vm.items.concat(searchResults))
        })

      Search.departments(query)
        .then(response => {
          let searchResults = response.response.docs.length > 0 ? response.response.docs : vm.noItem
          vm.$set(vm, 'items', vm.items.concat(searchResults))
        })
    },

    /**
     * Go to the selected route.
     */
    selected (item) {
      if (item.uuid == null) return
      this.items = []
      this.$router.push({ name: this.routeName, params: { uuid: item.uuid } })
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
