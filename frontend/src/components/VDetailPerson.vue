<template>
  <div>
        <b-list-group>
          <b-list-group-item class="header-item active">
            <icon class="icon-color" name="user"/>
            {{result.name}}
          </b-list-group-item>
        </b-list-group>

    <div v-if="result.locations" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          Adresse
        </b-list-group-item>
        <b-list-group-item>
          <icon name="phone"/>
          <span class="col">{{result.locations[1]}}</span>
        </b-list-group-item>
        <b-list-group-item>
          <icon name="map-marker-alt"/>
          <span class="col">{{result.locations[3]}}</span>
        </b-list-group-item>
        <b-list-group-item>
          <icon name="envelope"/>
          <span class="col">{{result.locations[5]}}</span>
        </b-list-group-item>
      </div>
    </div>

    <div class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          Afdeling
        </b-list-group-item>
        <b-list-group-item>
          <v-tree-view/>
        </b-list-group-item>
      </div>
    </div>

    <div v-if="result.managing" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          Ledertilknytninger
        </b-list-group-item>
        <b-list-group-item>
          {{result.managing[2]}} -
          <router-link :to="{ name: 'organisation' }">
            {{result.managing[0]}}
          </router-link>
        </b-list-group-item>
      </div>
    </div>

    <div v-if="result.associated" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          Tilknyttet enheder
        </b-list-group-item>
        <b-list-group-item>
          {{result.associated[2]}} -
          <router-link :to="{ name: 'organisation' }">
            {{result.associated[0]}}
          </router-link>
        </b-list-group-item>
      </div>
    </div>
  </div>
</template>

<script>
import VTreeView from '@/components/VTreeView'
import Search from '@/api/Search'

export default {
  name: 'VDetailPerson',

  components: {
    VTreeView
  },

  props: {
    uuid: String,
    result: Object
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
