<template>
  <b-form>
    <div class="mb-2 form-row">
      <v-search-option class="col-10" @change-option="updateSelection"/>
    </div>

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
  </b-form>
</template>

<script>
import { SearchMultipleFields } from '@/api/SearchMultipleFields'
import GetSearchFields from '@/mixins/GetSearchFields'
import GetFilterSelectedOption from '@/mixins/GetFilterSelectedOption'
import VSearchBarTemplate from './VSearchBarTemplate'
import VSearchOption from './VSearchOption'
import VAutocomplete from 'v-autocomplete'
import '../../node_modules/v-autocomplete/dist/v-autocomplete.css'
import { mapGetters } from 'vuex'

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
      template: VSearchBarTemplate,
      /**
       * The noItem value.
       * Used to give a default name.
       */
      noItem: [
        {
          document: JSON.stringify({
            name: 'Ingen resultater matcher din søgning',
            type: 'noresult_placeholder',
            clickable: false
          })
        }
      ]
    }
  },

  mixins: [GetSearchFields, GetFilterSelectedOption],

  computed: {
    ...mapGetters({
      searchItems: 'searchResults/GET_ITEMS'
    })
  },

  methods: {
    /**
     * Update employee or organisation suggestions based on search query.
     */
    updateItems (inputVal) {
      inputVal = inputVal.trim()
      let vm = this
      let fields = ['name', 'locations', 'departments']

      if (this.selectedOption == "job_titles"){
        fields = ['departments']
      }
      if (this.selectedOption == "emails"){
        fields = ['locations']
      }
      if (this.selectedOption == "phone_numbers"){
        fields = ['locations']
      }
      if (this.selectedOption == "persons"){
        fields = ['name']
      }
      if (this.selectedOption == "departments"){
        fields = ['name']
      }

      SearchMultipleFields(inputVal, fields)
        .then(res => {
          let results = []
          res.forEach(result => {
            results = results.concat(result)
          })

          /**
         * If we are searching within a specific field, we need only to return results
         * where inputVal was within that specific field.
         */
          results = this.getFilterSelectedOption(this.selectedOption, results, inputVal)

          if (!results.length) {
            results = results.concat(vm.noItem)
          }

          /**
         * We need to use Vue.set() to update the searchItems object,
         * because otherwise searchItems would no longer be reactive.
         */
          vm.$store.commit('searchResults/SET_SEARCH', results)
        })
        .catch(() => {
          vm.$store.commit('searchResults/SET_SEARCH', vm.noItem)
        })
    },

    /**
     * Go to the selected route.
     */
    selected (searchResult) {
      const parsedDocument = JSON.parse(this.item.document)
      if (!parsedDocument.hasOwnProperty('clickable')) {
        if (JSON.parse(this.item.document).parent) {
          this.$router.push({ name: 'organisation', params: { uuid: JSON.parse(searchResult.document).uuid } })
        } else {
          this.$router.push({ name: 'person', params: { uuid: JSON.parse(searchResult.document).uuid } })
        }
      } else if (parsedDocument.clickable === false) {
        this.$refs.searchWord.searchText = ''
      }
    },

    /**
     * View all search results for the given search string
     */
    viewSearchResults () {
      if (this.searchItems.length) {
        /**
         * this.$refs.searchWord poins to the v-autocomplete component.
         * Within this, we can get the current search string with searchText attribute.
         */
        this.$store.dispatch('searchResults/UPDATE_RESULTS')
        this.$router.push({ name: 'result', query: { fq: this.$refs.searchWord.searchText, criteria: this.selectedOption } })
      }
    },

    /**
     * Update which search criteria is selected, based on event value from child component.
     */
    updateSelection (val) {
      this.selectedOption = val
    }
  },

  mounted () {
    this.$refs.searchWord.searchText = this.$route.query.fq || ''
  }
}
</script>
