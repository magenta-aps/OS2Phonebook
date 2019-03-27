<template>
  <div>
    <b-form-select
      class="col"
      v-model="selected"
    >
      <option :value="null">{{ $t('department_option') }}</option>
      <option v-for="o in organisations" :key="o.uuid" :value="o.uuid">
        {{o.name}}
      </option>
    </b-form-select>
  </div>
</template>

<script>
import Search from '@/api/Search'

export default {
  name: 'SearchOption',

  data () {
    return {
      selected: null,
      organisations: []
    }
  },

  created () {
    this.getOrganisations()
  },

  methods: {
    getOrganisations () {
      let vm = this
      Search.roots()
        .then(res => {
          vm.organisations = res.response.docs.map(doc => {
            return JSON.parse(doc.document)
          })
        })
    }
  },

  watch: {
    selected (val) {
      this.$emit('change-option', val)
    }
  }
}
</script>
