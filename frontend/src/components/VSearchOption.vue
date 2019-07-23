<template>
  <div>
    <b-form-group class="col">
      <b-form-radio-group v-model="selected">
        <b-form-radio value="departments">
          {{ $t('searchOptions.departments') }}
        </b-form-radio>
        <b-form-radio value="emails">
          {{ $t('searchOptions.emails') }}
        </b-form-radio>
        <b-form-radio>
          {{ $t('searchOptions.tasks') }}
        </b-form-radio>
        <b-form-radio value="persons">
          {{ $t('searchOptions.employees') }}
        </b-form-radio>
        <b-form-radio value="job_titles">
          {{ $t('searchOptions.job_titles') }}
        </b-form-radio>
        <b-form-radio value="phone_numbers">
          {{ $t('searchOptions.phone_numbers') }}
        </b-form-radio>
      </b-form-radio-group>
    </b-form-group>
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
