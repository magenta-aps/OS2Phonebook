<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
      </div>
    </div>

    <h4 v-if="items.length" class="mt-3 mb-2 ml-2">{{ $t('results') }}</h4>
    <h4 v-if="!items.length" class="mt-3 mb-2 ml-2">{{ $t('no_results') }}</h4>

    <div class="card mt-2 mb-2" v-for="item in items" :key="item.uuid" v-if="!item.parent">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'person', params: { uuid: item.uuid } }">
          <b-list-group>
            <b-list-group-item class="bg-light">
              {{ item.name }}
            </b-list-group-item>
          <div v-if="item.locations && item.locations.length">
            <b-list-group-item v-for="(location, index) in item.locations" :key="item.locations[index][0]">
              <icon class="mb-1" v-if="getIcon(location[0])" :name="getIcon(location[0])"/>
              <span class="col">{{ location[1] }}</span>
            </b-list-group-item>
          </div>
          </b-list-group>
        </router-link>
      </div>
    </div>

    <div class="card mt-2 mb-2" v-for="item in items" :key="item.uuid" v-if="item.parent">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'organisation', params: { uuid: item.uuid } }">
        <b-list-group>
          <b-list-group-item class="bg-light">
            {{item.name}}
          </b-list-group-item>
          <div v-if="item.locations && item.locations.length">
          <b-list-group-item v-for="(location, index) in item.locations" :key="item.locations[index][0]">
            <icon class="mb-1" v-if="getIcon(location[0])" :name="getIcon(location[0])"/>
            <span class="col">{{ location[1] }}</span>
          </b-list-group-item>
          </div>
        </b-list-group>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import VSearch from '@/components/VSearch'
import VSearchOption from '@/components/VSearchOption'
import GetIcon from '@/mixins/GetIcon'

export default {
  name: 'Result',

  mixins: [GetIcon],

  components: {
    VSearch,
    VSearchOption
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
  }
}
</script>

<style scoped>
.link-color {
  color: #212529;
  text-decoration: none;
}
</style>
