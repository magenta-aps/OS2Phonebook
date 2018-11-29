<template>
  <div>
    <span>{{ parsedItem.name }}</span>
  </div>
</template>

<script>
export default {
  props: {
    item: { required: true }
  },

  computed: {
    parsedItem () {
      return JSON.parse(this.item.document)
    }
  }
}
</script>
