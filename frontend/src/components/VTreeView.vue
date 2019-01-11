<template>
  <div class="orgunit-tree">
    <liquor-tree
      v-if="treeData"
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
      return 'VTreeView' + this._uid
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
          let parsedResults = res.response.docs.map(d => JSON.parse(d.document))
          parsedResults.forEach(d => {
            const parentUuid = d.parent
            let parentDoc = parsedResults.find(parent => {
              return parent.uuid === parentUuid
            })
            if (parentDoc) {
              if (parentDoc.hasOwnProperty('children')) {
                parentDoc.children.push(d)
              } else {
                parentDoc.children = [d]
              }
            }
          })
          // remove all non-root items from the 0th level of the tree, as they have been added as children.
          parsedResults = parsedResults.filter(doc => doc.parent === 'ROOT')
          this.treeData = parsedResults
          this.treeData = parsedResults.map(d => {
            return {
              'id': d.uuid,
              'text': d.name,
              'data': d,
              'children': (d.children || []).map(function recursive (child) {
                return {
                  'id': child.uuid,
                  'text': child.text,
                  'data': child,
                  'children': child.children
                }
              })
            }
          })
        })
    },

    /**
     * Go to the selected route.
     */
    goToRoute () {
      console.log(this.treeData[0].id)
      this.$router.push({ name: 'organisation', params: { uuid: this.treeData[0].id } })
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
