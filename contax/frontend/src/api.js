// import Vue from 'vue'
import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000/',
  json: true
})

export default {
  async execute (method, resource, data) {
    return client({
      method,
      url: resource,
      data
    //   headers: {
    //     Authorization: `Bearer ${accessToken}`
    //   }
    }).then(req => {
      return req.data
    })
  },
  // Contacts
  getContacts () {
    return this.execute('get', 'api/contacts/')
  },
  getContact (id) {
    return this.execute('get', `api/contacts/${id}`)
  },
  createContact (data) {
    return this.execute('post', 'api/contacts/', data)
  },
  updateContact (id, data) {
    return this.execute('put', `api/contacts/${id}`, data)
  },
  deleteContact (id) {
    return this.execute('delete', `api/contacts/${id}`)
  },
  // Addresses
  getAddresses () {
    return this.execute('get', 'api/postal_addresses/')
  },
  getAddress (id) {
    return this.execute('get', `api/postal_addresses/${id}`)
  },
  createAddress (data) {
    return this.execute('post', 'api/postal_addresses/', data)
  },
  updateAddress (id, data) {
    return this.execute('put', `api/postal_addresses/${id}`, data)
  },
  deleteAddress (id) {
    return this.execute('delete', `api/postal_addresses/${id}`)
  }
}
