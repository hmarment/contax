<template>
  <div>
    <b-container class="container-fluid mt-4">
      <b-card-group deck v-for="(contact_group, count) in contacts" v-bind:key="count">
        <b-card v-for="contact in contact_group" v-bind:key="contact.id"
          style="max-width: 22rem;"
          class="mb-3"
        >
            <b-card-title>{{ contact.first_name + ' ' + contact.last_name }}</b-card-title>
            <b-card-sub-title class="mb-2"> {{ contact.date_of_birth }} </b-card-sub-title>
            <b-list-group flush v-if="contact.email_addresses.length > 0">
              <br>
              <span><b>Email Addresses</b></span>
              <b-list-group-item v-for="email in contact.email_addresses" v-bind:key="email.name"><b>{{ email.name }}:</b> {{ email.email_address }}</b-list-group-item>
            </b-list-group>
            <b-list-group flush v-if="contact.phone_numbers.length > 0">
              <br>
              <span><b>Phone Numbers</b></span>
              <b-list-group-item v-for="phone in contact.phone_numbers" v-bind:key="phone.name"><b>{{ phone.name }}:</b> {{ phone.phone_number }}</b-list-group-item>
            </b-list-group>
            <b-list-group flush v-if="contact.postal_addresses.length > 0">
              <br>
              <span><b>Addresses</b></span>
              <b-list-group-item v-for="address in contact.postal_addresses" v-bind:key="address.name">
                <b>{{ address.name }}</b>
                <b-card-text>
                  {{ address.street }}
                  <br>
                  {{ address.post_code }} {{ address.city }}
                  <br>
                  {{ address.country }}
                </b-card-text>
              </b-list-group-item>
            </b-list-group>
          <br>
          <b-button :href="('#/contacts/edit/' + contact.id)" variant="primary">Edit</b-button>
        </b-card>
      </b-card-group>
    </b-container>
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
      var contacts = await api.getContacts()
      var i
      var j
      var chunkedContacts = []
      var chunkSize = 3
      for (i = 0, j = contacts.length; i < j; i += chunkSize) {
        chunkedContacts.push(contacts.slice(i, i + chunkSize))
      }
      this.contacts = chunkedContacts
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
