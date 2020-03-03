<template>
    <div class="pt-5">
        <div v-if="contacts.length > 0">
            <div class="card mb-3" v-for="contact of this.contacts" v-bind:key="contact.id">
                <div class="row no-gutters">
                    <div class="col-md-4">
                        <svg class="bd-placeholder-img" width="200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail"><title>{{ contact.first_name + ' ' + contact.last_name }}</title><rect width="100%" height="100%" fill="#55595c"/><text x="50%" y="50%" fill="#eceeef" dy=".3em">{{ contact.first_name.charAt(0) }}</text></svg>
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h5 class="card-title">{{ contact.first_name + ' ' + contact.last_name }}</h5>
                            <p v-if="contact.email_addresses.length > 0" class="card-text">{{ contact.email_addresses[0].email_address }}</p>
                            <router-link :to="{name: 'edit', params: { id: contact.id }}" class="btn btn-sm btn-primary">Edit</router-link>
                            <button class="btn btn-danger btn-sm ml-1" v-on:click="deleteContact(contact)">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <p  v-if="contacts.length == 0">No contacts</p>
    </div>
</template>
<script>

import axios from 'axios'

export default {
  data () {
    return {
      contacts: []
    }
  },
  created () {
    this.all()
  },
  methods: {
    deleteContact: function (cntct) {
      if (confirm('Delete ' + cntct.first_name + ' ' + cntct.last_name)) {
        axios.delete(`http://127.0.0.1:8000/api/contacts/${cntct.id}`)
          .then(response => {
            this.all()
          })
      }
    },
    all: function () {
      axios.get('http://127.0.0.1:8000/api/contacts/')
        .then(response => {
          this.contacts = response.data
        })
    }
  }
}
</script>
