<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
        <v-search-option class="mt-3"/>
      </div>
    </div>

    <h4 class="mt-3 mb-2">Resultater</h4>
    <div class="card mt-2" v-for="item in items" :key="item.uuid" v-if="!item.parent">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'person', params: { uuid: item.uuid }}">
          <b-list-group>
            <b-list-group-item class="active">
                {{ item.name }}
            </b-list-group-item>
            <b-list-group-item v-if="item.locations">
              <icon name="phone"/>
              <span class="col">{{ item.locations[1] }}</span>
            </b-list-group-item>
            <b-list-group-item v-if="!item.locations">
              <icon name="phone"/>
              <span class="col">Ingen</span>
            </b-list-group-item>
          </b-list-group>
        </router-link>
      </div>
    </div>

    <div v-for="item in items" :key="item.uuid" v-if="item.parent" class="card mt-2 mb-2">
      <div class="card-body">
        <router-link class="link-color" :to="{ name: 'organisation', params: { result: item }}">
        <b-list-group>
          <b-list-group-item class="active">
            {{item.name}}
            <!-- <b-btn v-b-toggle.collapse1 variant="primary" class="float-right"><icon name="angle-down"/></b-btn> -->
          </b-list-group-item>
          <b-list-group-item v-if="item.locations">
            <icon name="phone"/>
            <span class="col mb-3">{{item.locations[1]}}</span>
          </b-list-group-item>
          <b-list-group-item v-if="!item.locations">
            <icon name="phone"/>
            <span class="col mb-3">Ingen</span>
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
    results: Array
  },

  computed: {
    items () {
      return this.results
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
