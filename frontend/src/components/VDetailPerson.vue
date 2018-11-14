<template>
  <div>
        <b-list-group>
          <b-list-group-item class="header-item active">
            <icon class="icon-color" name="user"/>
            Hans Pedersen
          </b-list-group-item>
        </b-list-group>

    <div class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
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
      </div>
    </div>

    <div class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Afdeling
          </b-list-group-item>
          <b-list-group-item>
            <v-tree-view/>
          </b-list-group-item>
      </div>
    </div>

    <div class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Ledertilknytninger
          </b-list-group-item>
          <b-list-group-item>
            Leder Digitalisering
          </b-list-group-item>
      </div>
    </div>

    <div class="card mt-2 mb-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Tilknyttet enheder
          </b-list-group-item>
          <b-list-group-item>
            IT afdelingen
          </b-list-group-item>
      </div>
    </div>
  </div>
</template>

<script>
import VTreeView from '@/components/VTreeView'

export default {
  name: 'VDetailPerson',

  components: {
    VTreeView
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

.header-item {
    font-size: 1.2em;
}
</style>
