import Vue from 'vue'
import Router from 'vue-router'
import Contacts from '@/components/Contacts'
import ContactEdit from '@/components/ContactEdit'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'contacts',
      component: Contacts
    },
    {
      path: '/contacts',
      name: 'contacts',
      component: Contacts
    },
    {
      path: '/contacts/edit/:id',
      name: 'edit',
      component: ContactEdit
    }
  ]
})
