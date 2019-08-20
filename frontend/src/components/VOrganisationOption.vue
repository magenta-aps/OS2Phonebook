<template>
  <div>
    <b-form-select
      class="col"
      v-model="selected"
    >
      <option :value="null">{{ $t('department_option') }}</option>
      <option v-for="o in organisations" :key="o.uuid" :value="o.root_uuid">
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
      organisations: []
    }
  },

  created () {
    this.getOrganisations()
  },

  computed: {
    selected: {
      get () {
        return this.$store.getters['searchResults/GET_SELECTED_ORG_OPTION']
      },
      set (value) {
        this.$store.commit('searchResults/SET_SELECTED_ORG_OPTION', value)
      }
    }
  },

  methods: {
    getOrganisations () {
      let vm = this
      Search.roots()
        .then(res => {
          vm.organisations = res
        })
    }
  },

  mounted () {
    let selectedOrgOption = this.$route.query.root
    if (selectedOrgOption) {
      this.selected = selectedOrgOption
    }
  }
}
</script>
