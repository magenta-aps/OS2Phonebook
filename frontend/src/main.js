import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import BootstrapVue from 'bootstrap-vue'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

require('../node_modules/bootstrap/dist/css/bootstrap.css')
require('../node_modules/bootstrap-vue/dist/bootstrap-vue')
require('@/assets/css/global.css')

Vue.config.productionTip = false

Vue.use(BootstrapVue)

Vue.component('icon', Icon)

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
