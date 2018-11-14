<template>
  <div>
    <b-form-select v-model="selected" class="col">
      <option :value="null" disabled>Vælg søgekriterier</option>
      <option>
          Afdelinger
      </option>
      <option>
          Email adresser
      </option>
      <option>
          Opgaver
      </option>
      <option>
          Personer
      </option>
      <option>
          Stillingsbetegnelser
      </option>
      <option>
          Telefonnummer
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
