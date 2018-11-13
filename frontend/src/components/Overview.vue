<template>
  <div>
    <div class="card">
      <div class="card-body">
        <search/>
      </div>
    </div>

    <div class="card mt-3">
      <div class="card-body">
        <h4>Overblik</h4>
        <tree-view/>
      </div>
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search'
import SearchOption from '@/components/SearchOption'
import TreeView from '@/components/TreeView'

export default {
  name: 'Overview',

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
</style>
