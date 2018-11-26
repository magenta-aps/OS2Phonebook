<template>
  <div>
    <b-list-group>
      <b-list-group-item class="header-item active">
        <icon class="icon-color" name="users"/>
        {{result.name}}
      </b-list-group-item>
    </b-list-group>

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

    <div v-if="result.locations" class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Lokationer
          </b-list-group-item>
          <b-list-group-item>
            <icon name="map-marker-alt"/>
            <span class="col">{{result.locations[1]}}</span>
          </b-list-group-item>
          <b-list-group-item>
            <icon name="phone"/>
            <span class="col">{{result.locations[3]}}</span>
          </b-list-group-item>
          <b-list-group-item>
            <icon name="envelope"/>
            <span class="col">{{result.locations[5]}}</span>
          </b-list-group-item>
      </div>
    </div>

    <div v-if="result.managers" class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Ledere
          </b-list-group-item>
          <b-list-group-item>
            {{result.managers[0]}} - {{result.managers[1]}}
          </b-list-group-item>
      </div>
    </div>

    <div v-if="result.employees" class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Ansatte
          </b-list-group-item>
          <b-list-group-item>
            {{result.employees}}
          </b-list-group-item>
      </div>
    </div>

    <div v-if="result.associated" class="card mt-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Tilknyttede
          </b-list-group-item>
          <b-list-group-item>
            {{result.associated}}
          </b-list-group-item>
      </div>
    </div>

    <div class="card mt-2 mb-2">
      <div class="card-body">
          <b-list-group-item variant="dark">
            Opgaver
          </b-list-group-item>
          <b-list-group-item>
            Ferieydelse optjent under barsel (34.30.10)
          </b-list-group-item>
          <b-list-group-item>
            Ferieydelse optjent under barsel (34.30.10)
          </b-list-group-item>
      </div>
    </div>
  </div>
</template>

<script>
import VTreeView from '@/components/VTreeView'

export default {
  name: 'VDetailOrganisation',

  components: {
    VTreeView
  },

  props: {
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
