import Vue from 'vue'
import Router from 'vue-router'
import Overview from '@/components/VOverview'
import Result from '@/components/VResult'
import Person from '@/components/VDetailPerson'
import Organisation from '@/components/VDetailOrganisation'
import Search from '@/api/Search'

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
      component: Result,
      props: true
    },
    {
      path: '/person/:uuid',
      name: 'person',
      component: Person,
      props: true,
      beforeEnter (to, from, next) {
        Search.employees('uuid', to.params.uuid)
          .then(res => {
            to.params.result = res[0]
            return res
          })
          .finally(() =>
            next()
          )
      }
    },
    {
      path: '/organisation/:uuid',
      name: 'organisation',
      component: Organisation,
      props: true
    }
  ]
})
