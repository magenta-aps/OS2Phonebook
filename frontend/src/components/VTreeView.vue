<template>
  <div class="orgunit-tree">
    <liquor-tree
      v-if="treeData"
      :ref="nameId"
      id="nodeTree"
      :data="treeData"
      :options="treeOptions"
    >

      <div class="tree-scope" slot-scope="{ node }" v-on:click.prevent="goToRoute">
        <template>
          <icon name="users"/>

          <span class="text">
            {{ node.text }}
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
      selected: undefined,
      treeOptions: {
        propertyNames: {
          text: 'name',
          id: 'uuid'
        }
      }
    }
  },

  created () {
    this.getTreeData()
  },

  methods: {
    getTreeData () {
      TreeData.treeView('uuid')
        .then(res => {
          let parsedResults = res
          let dataMap = parsedResults.reduce(function (map, node) {
            map[node.uuid] = node
            return map
          }, {})

          let tree = []
          parsedResults.forEach(function (node) {
            // add to parent
            let parent = dataMap[node.parent]
            if (parent) {
              // create child array if it doesn't exist
              (parent.children || (parent.children = []))
              // add node to child array
                .push(node)
            } else {
              // parent is null or missing
              tree.push(node)
            }
          })

          // Sorting the data in SOLR requires extensions to the schema, due
          // to the way the 'name' field is tokenized for searching. Sorting
          // in the UI has minimal performance impact so it should be good enough.
          let sortTree = tree => {
            tree.forEach(node => {
              let children = node.children
              if (children) {
                children.sort((a, b) => {
                  return a.name.localeCompare(b.name, 'da')
                })
                sortTree(children)
              }
            })
          }
          sortTree(tree)

          // remove all non-root items from the 0th level of the tree, as they have been added as children.
          this.treeData = tree
        })
    },

    /**
     * Go to the selected route.
     */
    goToRoute () {
      this.$router.push({ name: 'organisation', params: { uuid: this.tree.selected()[0].id } })
    }
  },

  updated () {
    // when the tree has mounted, find the element we should select, according to UUID in URL param
    this.tree.$on('tree:mounted', () => {
      if (this.$route.params.uuid) {
        let openedNode = this.tree.find({ id: this.$route.params.uuid })
        if (openedNode) {
          openedNode.forEach(n => {
            n.select()
            n.expandTop()
          })
        }
      }
    })
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
    background: #007bff!important
  }
  .tree-node.selected > .tree-content > .tree-anchor {
    color: #fff;
  }
</style>
