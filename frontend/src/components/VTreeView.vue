<template>
  <div class="orgunit-tree">
    <liquor-tree v-if="treeData"
      :ref="nameId"
      :data="treeData"
    >

      <div class="tree-scope" slot-scope="{ node }" v-on:click.prevent="goToRoute">
        <template>
          <icon name="users"/>

          <span class="text">
            {{ node.data.name }}
          </span>
        </template>
      </div>
    </liquor-tree>
  </div>
</template>

<script>
import LiquorTree from 'liquor-tree'
import TreeData from '@/api/Search'

export default {
  components: {
    LiquorTree
  },

  computed: {
    nameId () {
      return 'moTreeView' + this._uid
    },

    tree () {
      return this.$refs[this.nameId]
    }
  },

  data () {
    return {
      treeData: null,
      selected: undefined
    }
  },

  created () {
    this.getTreeData()
  },

  methods: {
    getTreeData () {
      TreeData.treeView('uuid')
        .then(res => {
          this.treeData = res.response.docs.map(function (d) {
            let doc = JSON.parse(d.document)
            return {
              'id': doc.uuid,
              'text': doc.name,
              'data': doc,
              'children': [doc.parent]
            }
          })
        })
    },

    /**
     * Go to the selected route.
     */
    goToRoute () {
      console.log(this.treeData)
      this.$router.push({ name: 'organisation', params: { uuid: this.node } })
    }
  }

}
</script>

<!-- this particular styling is not scoped, otherwise liqour tree cannot detect the overwrites -->
<style>
  .tree > .tree-root, .tree-content {
     padding: 0;
   }
   .tree-children {
     transition-timing-function: ease-in-out;
     transition-duration: 150ms;
   }
  .tree-node.selected > .tree-content {
    background: #007bff;
  }
  .tree-node.selected > .tree-content > .tree-anchor {
    color: #fff;
  }
</style>
