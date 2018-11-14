import Vue from 'vue'
import Router from 'vue-router'
import Overview from '@/components/VOverview'
import Result from '@/components/VResult'
import Person from '@/components/VDetailPerson'
import Organisation from '@/components/VDetailOrganisation'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Overview
    },
    {
      path: '/result',
      name: 'result',
      component: Result
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import(/* webpackChunkName: "result" */ './views/Result.vue')
    },
    {
      path: '/person',
      name: 'person',
      component: Person
    },
    {
      path: '/organisation',
      name: 'organisation',
      component: Organisation
    }
  ]
})
