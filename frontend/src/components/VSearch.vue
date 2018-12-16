<template>
  <b-form>
    <div class="form-row">
      <v-autocomplete
        class="col"
        type="search"
        :placeholder="$t('search')"
        :items="searchItems"
        v-model="item"
        ref="searchWord"
        :component-item='template'
        @item-clicked="selected(item)"
        @update-items="updateItems"
        :auto-select-one-item="false"
        :min-len="2"
      />

      <b-button class="float-right col-2 bg-primary" type="submit" v-on:click.prevent="viewSearchResults">
        <icon name="search"/>
      </b-button>
    </div>

    <div class="mt-2 form-row">
      <v-search-option v-model="selectedOption" class="col-10"/>
    </div>
  </b-form>
</template>

<script>
import { SearchMultipleFields } from '@/api/SearchMultipleFields'
import VSearchBarTemplate from './VSearchBarTemplate'
import VSearchOption from './VSearchOption'
import VAutocomplete from 'v-autocomplete'
import '../../node_modules/v-autocomplete/dist/v-autocomplete.css'

export default {
  name: 'Search',

  components: {
    VAutocomplete,
    VSearchOption
  },

  data () {
    return {
      selectedOption: null,
      item: null,
      searchItems: [],
      template: VSearchBarTemplate,
      /**
       * The noItem component value.
       * Used to give a default name.
       */
      noItem: [
        {
          document: JSON.stringify({
            name: 'Ingen resultater matcher din søgning'
          })
        }
      ]
    }
  },

  methods: {
    /**
     * Update employee or organisation suggestions based on search query.
     */
    updateItems (inputVal) {
      let vm = this
      vm.searchItems = []

      SearchMultipleFields(inputVal, ['name', 'locations', 'departments'])
        .then(res => {
          let results = []
          res.forEach(result => {
            results = results.concat(result)
          })
          if (!results.length) {
            results = results.concat(vm.noItem)
          }
          // We need to use Vue.set() to update the searchItems object, because otherwise searchItems would no longer be reactive.
          vm.$set(vm, 'searchItems', results)
        })
        .catch(() => {
          vm.$set(vm, 'searchItems', vm.noItem)
        })
    },

    /**
     * Go to the selected route.
     */
    selected (searchResult) {
      if (JSON.parse(this.item.document).parent) {
        this.$router.push({ name: 'organisation', params: { uuid: JSON.parse(searchResult.document).uuid } })
      } else {
        this.$router.push({ name: 'person', params: { uuid: JSON.parse(searchResult.document).uuid } })
      }
    },

    /**
     * View all search results for the given search string
     */
    viewSearchResults () {
      if (this.searchItems.length) {
        // this.$refs.searchWord poins to the v-autocomplete component.
        // Within this, we can get the current search string with searchText attribute.
        this.$router.push({ name: 'result', query: { q: this.$refs.searchWord.searchText } })
      }
    }
  }
}
</script>
