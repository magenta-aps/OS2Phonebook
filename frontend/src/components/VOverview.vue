<template>
  <div>
    <div class="card">
      <div class="card-body">
        <v-search/>
      </div>
    </div>

    <div class="card mt-3">
      <div class="card-body">
        <h4>
          <icon class="icon-color" name="folder-open"/>
          {{ $t('overview') }}
        </h4>
        <v-tree-view/>
      </div>
    </div>
  </div>
</template>

<script>
import VSearch from '@/components/VSearch'
import VTreeView from '@/components/VTreeView/VTreeView'

export default {
  name: 'Overview',

  components: {
    VSearch,
    VTreeView
  }
}
</script>
