<template>
  <div>
    <span>{{ item.name[0] }}</span>
  </div>
</template>

<script>
export default {
  props: {
    item: { required: true }
  }
}
</script>
