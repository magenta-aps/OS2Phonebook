<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
        <v-search-option class="mt-3"/>
      </div>
    </div>

    <h4 class="mt-3 mb-2">Resultater</h4>
    <div class="card mt-2">
      <div class="card-body">
        <router-link
          :to="{ name: 'person'}"
        >
          <b-list-group>
            <b-list-group-item class="active">
                Hans Pedersen
            </b-list-group-item>
            <b-list-group-item>
              <icon name="phone"/>
              <span class="col">34233350</span>
            </b-list-group-item>
          </b-list-group>
        </router-link>
      </div>
      </div>

    <div class="card mt-2">
      <div class="card-body">
        <b-list-group>
          <b-list-group-item class="active">Mia Larsen</b-list-group-item>
          <b-list-group-item>
            <icon name="envelope"/>
            <span class="col">mila@gmail.dk</span>
          </b-list-group-item>
        </b-list-group>
      </div>
    </div>

    <div class="card mt-2 mb-2">
      <div class="card-body">
        <router-link
          :to="{ name: 'organisation'}"
        >
        <b-list-group>
          <b-list-group-item class="active">
            <span class="float-left">Digitalisering</span>
            <b-btn v-b-toggle.collapse1 variant="primary" class="float-right"><icon name="angle-down"/></b-btn>
          </b-list-group-item>
          <b-list-group-item>
            <icon name="phone"/>
            <span class="col mb-3">34233350</span>
          </b-list-group-item>

          <b-collapse id="collapse1">
            <b-list-group-item>
              <b-list-group-item variant="dark">Afdeling</b-list-group-item>
              <v-tree-view/>
            </b-list-group-item>
          </b-collapse>
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
