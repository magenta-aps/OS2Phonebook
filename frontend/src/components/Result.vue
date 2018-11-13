<template>
  <div>
    <div class="card">
      <div class="card-body">
        <search/>
        <search-option class="mt-3"/>
      </div>
    </div>

    <div class="card mt-3 mb-3">
      <div class="card-body">
        <h4>Resultater</h4>
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

        <b-list-group class="mt-3">
          <b-list-group-item class="active">Mia Larsen</b-list-group-item>
          <b-list-group-item>
            <icon name="envelope"/>
            <span class="col">mila@gmail.dk</span>
          </b-list-group-item>
        </b-list-group>

        <router-link
          :to="{ name: 'organization'}"
        >
        <b-list-group class="mt-3">
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
              <tree-view/>
            </b-list-group-item>
          </b-collapse>
        </b-list-group>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search'
import SearchOption from '@/components/SearchOption'
import TreeView from '@/components/TreeView'

export default {
  name: 'Result',

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
