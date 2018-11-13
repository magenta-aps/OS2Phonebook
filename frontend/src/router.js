import Vue from 'vue'
import Router from 'vue-router'
import Overview from '@/components/Overview'
import Result from '@/components/Result'
import Person from '@/components/DetailPerson'
import Organization from '@/components/DetailOrganization'

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
      path: '/organization',
      name: 'organization',
      component: Organization
    }
  ]
})
