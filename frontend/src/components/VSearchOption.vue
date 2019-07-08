<template>
  <div>
    <b-form-select v-model="selected" class="col">
      <option :value="null">{{ $t('searchOptions.search_criteria_option') }}</option>
      <option value="departments">
        {{ $t('searchOptions.departments') }}
      </option>
      <option value="emails">
        {{ $t('searchOptions.emails') }}
      </option>
      <option>
        {{ $t('searchOptions.tasks') }}
      </option>
      <option value="persons">
        {{ $t('searchOptions.employees') }}
      </option>
      <option value="job_titles">
        {{ $t('searchOptions.job_titles') }}
      </option>
      <option value="phone_numbers">
        {{ $t('searchOptions.phone_numbers') }}
      </option>
    </b-form-select>
  </div>
</template>

<script>
export default {
  name: 'SearchOption',

  computed: {
    selected: {
      get () {
        return this.$store.getters['searchResults/GET_SELECTED_CRITERIA_OPTION']
      },
      set (value) {
        this.$store.commit('searchResults/SET_SELECTED_CRITERIA_OPTION', value)
      }
    }
  },
  mounted () {
    let selectedCriteria = this.$route.query.criteria
    if (selectedCriteria) {
      this.selected = selectedCriteria
    }
  }

}
</script>
