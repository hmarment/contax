import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import ContactEdit from '@/components/ContactEdit'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/contacts',
      name: 'contacts',
      component: Index
    },
    {
      path: '/contacts/edit/:id',
      name: 'edit',
      component: ContactEdit
    }
  ]
})
