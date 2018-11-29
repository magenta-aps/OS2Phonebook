<template>
  <div>
        <b-list-group>
          <b-list-group-item class="header-item active">
            <icon class="mb-1" name="user"/>
            {{result.name}}
          </b-list-group-item>
        </b-list-group>

    <div v-if="result.locations.length" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          {{ $t('contact_info') }}
        </b-list-group-item>
        <b-list-group-item v-if="result.locations && result.locations.length" v-for="(location, idx) in result.locations" :key="Object.keys(location)[idx]">
          <icon  class="mb-1" v-if="getIcon(location[0])" :name="getIcon(location[0])"/>
          <span class="col">{{ location[1] }}</span>
        </b-list-group-item>
      </div>
    </div>

    <div class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          {{ $t('department') }}
        </b-list-group-item>
        <b-list-group-item>
          <v-tree-view/>
        </b-list-group-item>
      </div>
    </div>

    <div v-if="result.managing.length" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          {{ $t('managing') }}
        </b-list-group-item>
        <b-list-group class="mb-2" v-for="val in result.managing" :key="val[1]">
          <b-list-group-item>
            <router-link :to="{ name: 'organisation', params: { uuid: val[1] } }">
              {{val[0]}}
            </router-link>
          </b-list-group-item>
          <b-list-group-item>
            {{val[2]}}
          </b-list-group-item>
        </b-list-group>
      </div>
    </div>

    <div v-if="result.associated.length" class="card mt-2 mb-2">
      <div class="card-body">
        <b-list-group-item variant="dark">
          {{ $t('associated_departments') }}
        </b-list-group-item>
        <b-list-group class="mb-2" v-for="val in result.associated" :key="val[1]">
          <b-list-group-item>
            <router-link :to="{ name: 'organisation', params: { uuid: val[1] } }">
              {{val[0]}}
            </router-link>
          </b-list-group-item>
          <b-list-group-item>
            {{val[2]}}, {{val[3]}}
          </b-list-group-item>
        </b-list-group>
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
  },

  props: {
    uuid: String,
    result: Object
  },

  methods: {
    getIcon (locationType) {
      if (locationType === 'PHONE') {
        return 'phone'
      } else if (locationType === 'DAR') {
        return 'map-marker-alt'
      } else if (locationType === 'EMAIL') {
        return 'envelope'
      }
      return null
    }
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
