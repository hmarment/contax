<template>
  <div class="container-fluid mt-4">
    <h1 class="h1">Contacts</h1>
    <b-alert :show="loading" variant="info">Loading...</b-alert>
    <b-row>
      <b-col>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Date of Birth</th>
              <th>Updated At</th>
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contact in contacts" :key="contact.id">
              <td>{{ contact.id }}</td>
              <td>{{ contact.first_name }}</td>
              <td>{{ contact.last_name }}</td>
              <td>{{ contact.date_of_birth }}</td>
              <td>{{ contact.last_updated }}</td>
              <td class="text-right">
                <a href="#" @click.prevent="populateContactToEdit(contact)">Edit</a> -
                <a href="#" @click.prevent="deleteContact(contact.id)">Delete</a>
              </td>
            </tr>
          </tbody>
        </table>
      </b-col>
      <b-col lg="3">
        <b-card :title="(model.id ? 'Edit Contact ID#' + model.id : 'New Post')">
          <form @submit.prevent="saveContact">
            <b-form-group label="First Name">
              <b-form-input type="text" v-model="model.first_name"></b-form-input>
            </b-form-group>
            <b-form-group label="Last Name">
              <b-form-input type="text" v-model="model.last_name"></b-form-input>
            </b-form-group>
            <b-form-group label="Date of Birth">
              <b-form-input type="text" v-model="model.date_of_birth"></b-form-input>
            </b-form-group>
            <div>
              <b-btn type="submit" variant="success">Save Contact</b-btn>
            </div>
          </form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import api from '@/api'
export default {
  data () {
    return {
      loading: false,
      contacts: [],
      model: {}
    }
  },
  async created () {
    this.refreshContacts()
  },
  methods: {
    async refreshContacts () {
      this.loading = true
      this.contacts = await api.getContacts()
      this.loading = false
    },
    async populateContactToEdit (contact) {
      this.model = Object.assign({}, contact)
    },
    async saveContact () {
      if (this.model.id) {
        await api.updateContact(this.model.id, this.model)
      } else {
        await api.createContact(this.model)
      }
      this.model = {} // reset form
      await this.refreshContacts()
    },
    async deleteConact (id) {
      if (confirm('Are you sure you want to delete this contact?')) {
        // if we are editing a contact we deleted, remove it from the form
        if (this.model.id === id) {
          this.model = {}
        }
        await api.deleteConact(id)
        await this.refreshContacts()
      }
    }
  }
}
</script>
