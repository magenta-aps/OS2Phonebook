<template>
  <div>
    <div class="card mt-3 mb-3">
      <div class="card-body">
        <b-list-group>
          <b-list-group-item class="active">Hans Pedersen</b-list-group-item>
          <b-list-group-item>
          <b-list-group-item class="mt-3" variant="dark">
            Adresse
          </b-list-group-item>
          <b-list-group-item>
            <icon name="map-marker-alt"/>
            <span class="col">Hold-an vej 7</span>
          </b-list-group-item>
          <b-list-group-item>
            <icon name="phone"/>
            <span class="col">34233350</span>
          </b-list-group-item>
          <b-list-group-item>
            <icon name="envelope"/>
            <span class="col">mila@gmail.dk</span>
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Afdeling
          </b-list-group-item>
          <b-list-group-item>
            <tree-view/>
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Ledertilknytninger
          </b-list-group-item>
          <b-list-group-item>
            Leder Digitalisering
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Tilknyttet enheder
          </b-list-group-item>
          <b-list-group-item class="mb-3">
            IT afdelingen
          </b-list-group-item>
          </b-list-group-item>
        </b-list-group>
      </div>
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search'
import SearchOption from '@/components/SearchOption'
import TreeView from '@/components/TreeView'

export default {
  name: 'Overview',

  components: {
    Search,
    SearchOption,
    TreeView
  }
}
</script>

<style scoped>
.card-body {
  background-color: #ffffff;
}

.list-group-item {
    padding: 0.25rem 0.5rem;
}
</style>
