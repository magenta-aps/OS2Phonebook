<template>
  <div>
    <b-form-select v-model="selected" class="col">
      <option :value="null" disabled>Vælg søgekriterier</option>
      <option>
        {{ $t('searchOptions.departments') }}
      </option>
      <option>
        {{ $t('searchOptions.emails') }}
      </option>
      <option>
        {{ $t('searchOptions.tasks') }}
      </option>
      <option>
        {{ $t('searchOptions.employees') }}
      </option>
      <option>
        {{ $t('searchOptions.job_titles') }}
      </option>
      <option>
        {{ $t('searchOptions.phone_numbers') }}
      </option>
    </b-form-select>
  </div>
</template>

<script>
export default {
  name: 'SearchOption',

  data () {
    return {
      selected: null
    }
  }
}
</script>
