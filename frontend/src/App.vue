<template>
  <div id="app">
    <router-link :to="{ name: 'home'}">
      <b-navbar class="bg-primary">
        <b-navbar-brand class="mx-auto"><span class="text-color">{{ $t('phonebook') }}</span></b-navbar-brand>
      </b-navbar>
    </router-link>

    <main class="container container-fluid container-top-margin">
      <router-view/>
    </main>
  </div>
</template>

<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .container-top-margin {
    margin-top: 1em;
  }

  .text-color {
    color: #ffffff;
  }
</style>
