<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
      </div>
    </div>

    <h4 v-if="items.length" class="mt-3 mb-2 ml-2">{{ $t('results') }}</h4>
    <h4 v-if="!items.length" class="mt-3 mb-2 ml-2">{{ $t('no_results') }}</h4>

      <div
        class="card mt-2 mb-2"
        v-for="item in items" :key="item.uuid"
      >
        <!-- Employees -->
        <div class="card-body" v-if="!item.parent">
          <b-list-group>
            <router-link :to="{ name: 'person', params: { uuid: item.uuid } }">
              <b-list-group-item class="bg-light">
                {{ item.name }}
              </b-list-group-item>
            </router-link>
            <template v-if="item.departments && item.departments.length">
              <template v-for="department in item.departments">
                <b-list-group-item v-b-toggle="item.name" :key="department[1]">
                  <span>{{ department[3] }}</span>
                  <icon class="mt-1 float-right" name="info-circle"/>
                </b-list-group-item>
              </template>
            </template>
            <template v-if="item.departments && item.departments.length">
              <b-collapse :id="item.name">
                <template v-for="department in item.departments">
                  <b-list-group-item :key="department[1]">
                    <router-link class="link-color" :to="{ name: 'organisation', params: { uuid: department[1] } }">
                        <span>{{ department[0] }}</span>
                    </router-link>
                  </b-list-group-item>
                </template>
                <b-list-group-item v-for="(location, index) in item.locations" :key="item.locations[index][0]">
                  <icon class="mb-1" v-if="getPersonIcon(location[0])" :name="getPersonIcon(location[0])"/>
                  <span class="col">{{ location[1] }}</span>
                </b-list-group-item>
              </b-collapse>
            </template>
          </b-list-group>
        </div>

        <!-- Departments -->
        <div class="card-body" v-if="item.parent">
          <b-list-group>
            <router-link class="link-color" :to="{ name: 'organisation', params: { uuid: item.uuid } }">
              <b-list-group-item class="bg-light">
                {{ item.name }}
              </b-list-group-item>
            </router-link>
            <template v-if="item.locations && item.locations.length">
                <b-list-group-item
                  v-for="(location, index) in item.locations" :key="item.locations[index][0]"
                  :class="!getOrgIcon(location[0]) ? 'empty' : ''"
                >
                  <template v-if="getOrgIcon(location[0])">
                    <icon class="mb-1" :name="getOrgIcon(location[0])"/>
                    <span class="col">{{ location[3] }}</span>
                  </template>
                </b-list-group-item>
            </template>
          </b-list-group>
        </div>
      </div>
  </div>
</template>

<script>
import VSearch from '@/components/VSearch'
import GetIcon from '@/mixins/GetIcon'
import bCollapse from 'bootstrap-vue/es/components/collapse/collapse'
import bToggleDirective from 'bootstrap-vue/es/directives/toggle/toggle'
import { mapGetters } from 'vuex'

export default {
  name: 'Result',

  mixins: [GetIcon],

  components: {
    VSearch,
    'b-collapse': bCollapse
  },

  directives: {
    'b-toggle': bToggleDirective
  },

  props: {
    results: Array
  },

  data () {
    return {
      open: false
    }
  },

  computed: {
    ...mapGetters({
      items: 'searchResults/GET_FORMATTED_ITEMS'
    })
  }
}
</script>

<style scoped>
  .list-group-item.empty {
    display: none;
  }
</style>
