<template>
<div>
   <li class="item">
     <span @click="toggle">
        <icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/>
      </span>

      <router-link
        class="link-color"
        :to="{ name: 'result'}"
      >
        <icon class="icon-color" name="users"/>
        Ballerup Kommune
      </router-link>

      <span class="link-color">
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
        <br><icon class="icon" :name="open ? 'caret-down' : 'caret-right'"/><icon class="icon" name="users"/>
        Ballerup
      </span>

    <ul v-show="open">
      <icon class="icon" name="users"/>Ballerup
    </ul>
   </li>
</div>
</template>

<script>
export default {
  name: 'TreeView',

  data () {
    return {
      open: false
    }
  },

  methods: {
    toggle () {
      this.open = !this.open
    }
  }
}
</script>

<style scoped>
  ul {
    padding-left: 1.25rem;
  }

  .item {
    cursor: pointer;
    list-style-type: none;
    display: block;
    white-space: nowrap;
  }

  .icon {
    color: #343a40;
    width: 1rem;
    display: inline-block;
  }

  .link-color{
    color: #212529;
    text-decoration: none;
  }

  .link-color:hover{
    color: #007bff;
  }

  .router-link-active{
    color:#007bff;
  }
</style>
