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
  }
}
