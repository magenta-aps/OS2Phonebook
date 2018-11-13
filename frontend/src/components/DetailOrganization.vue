<template>
  <div>
    <div class="card mt-3 mb-3">
      <div class="card-body">
        <b-list-group>
          <b-list-group-item class="active">Digitalisering</b-list-group-item>
          <b-list-group-item>
          <b-list-group-item class="mt-3" variant="dark">
            Afdeling
          </b-list-group-item>
          <b-list-group-item>
            <tree-view/>
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Lokationer
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
            <span class="col">digitalisering@gmail.dk</span>
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Ledere
          </b-list-group-item>
          <b-list-group-item>
            Leder Jesper Torup
          </b-list-group-item>
          <b-list-group-item>
            Sekretær Bente Andersen
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Ansatte
          </b-list-group-item>
          <b-list-group-item>
            Allan Nielsen
          </b-list-group-item>
           <b-list-group-item>
            Ole Henrik Langgard
          </b-list-group-item>
          <b-list-group-item>
            Søren Petersen
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Tilknyttede
          </b-list-group-item>
          <b-list-group-item>
            Camilla Toft Sørensen
          </b-list-group-item>

          <b-list-group-item class="mt-3" variant="dark">
            Opgaver
          </b-list-group-item>
          <b-list-group-item>
            Ferieydelse optjent under barsel (34.30.10)
          </b-list-group-item>
          <b-list-group-item class="mb-3">
            Ferieydelse optjent under barsel (34.30.10)
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
