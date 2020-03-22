import Vue from 'vue'
import Router from 'vue-router'
import Contacts from '@/components/contacts/Contacts'
import ContactEdit from '@/components/contacts/ContactEdit'
import Addresses from '@/components/addresses/Addresses'

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
    },
    {
      path: '/addresses',
      name: 'addresses',
      component: Addresses
    }
  ]
})
