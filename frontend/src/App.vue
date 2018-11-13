<template>
  <div id="app">
    <router-link
      :to="{ name: 'home'}"
    >
      <b-navbar class="bg-primary">
        <b-navbar-brand class="mx-auto">{{ $t('phonebook') }}</b-navbar-brand>
      </b-navbar>
    </router-link>

    <main class="container-fluid container-top-margin">
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
</style>
