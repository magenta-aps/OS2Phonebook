<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
        <v-search-option class="mt-3"/>
      </div>
    </div>

    <h4 v-if="items.length" class="mt-3 mb-2">{{ $t('results') }}</h4>
    <h4 v-if="!items.length" class="mt-3 mb-2">{{ $t('no_results') }}</h4>

    <div class="card mt-2 mb-2" v-for="item in items" :key="item.uuid" v-if="!item.parent">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'person', params: { uuid: item.uuid } }">
          <b-list-group>
            <b-list-group-item class="active">
                {{ item.name }}
            </b-list-group-item>
            <b-list-group-item v-if="item.locations && item.locations.length" v-for="(location, idx) in item.locations" :key="item.locations[idx][0]">
              <icon class="mb-1" v-if="getIcon(location[0])" :name="getIcon(location[0])"/>
              <span class="col">{{ location[1] }}</span>
            </b-list-group-item>
          </b-list-group>
        </router-link>
      </div>
    </div>

    <div class="card mt-2 mb-2" v-for="item in items" :key="item.uuid" v-if="item.parent">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'organisation', params: { uuid: item.uuid } }">
        <b-list-group>
          <b-list-group-item class="active">
            {{item.name}}
          </b-list-group-item>
          <b-list-group-item v-if="item.locations && item.locations.length" v-for="(location, idx) in item.locations" :key="item.locations[idx][0]">
            <icon class="mb-1" v-if="getIcon(location[0])" :name="getIcon(location[0])"/>
            <span class="col">{{ location[1] }}</span>
          </b-list-group-item>
        </b-list-group>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import VSearch from '@/components/VSearch'
import VSearchOption from '@/components/VSearchOption'
import VTreeView from '@/components/VTreeView'

export default {
  name: 'Result',

  components: {
    VSearch,
    VSearchOption,
    VTreeView
  },

  props: {
    q: String,
    results: Array
  },

  computed: {
    items () {
      var results = []
      for (var item = 0; item < this.results.length; item++) {
        if (this.results[item].document) {
          results.push(JSON.parse(this.results[item].document))
        }
      }
      return results
    }
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

.link-color {
  color: #212529;
  text-decoration: none;
}
</style>
