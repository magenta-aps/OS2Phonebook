<template>
  <div id="app">
    <router-link :to="{ name: 'home'}">
      <b-navbar class="bg-primary" type="dark">
        <b-navbar-brand class="mx-auto">{{ $t('phonebook') }}</b-navbar-brand>
      </b-navbar>
    </router-link>

    <main class="container container-fluid mt-4">
      <router-view/>
    </main>
  </div>
</template>

<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
