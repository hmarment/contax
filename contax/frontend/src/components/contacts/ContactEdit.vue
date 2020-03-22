<template>
    <div>
    <b-container class="container-fluid mt-4">
      <b-card
        class="mb-3"
        title="Edit Contact"
        v-bind="contact"
      >
      <hr>
      <b-form @submit="saveContact">
        <b-form-group
            label-cols-lg="4"
            label="Contact Details"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-0"
          >
            <b-form-group
              label-cols-sm="3"
              label="First Name:"
              label-align-sm="right"
              label-for="first-name"
            >
              <b-form-input id="first-name" type="text" v-model="contact.first_name"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Last Name:"
              label-align-sm="right"
              label-for="last-name"
            >
              <b-form-input id="last-name" type="text" v-model="contact.last_name"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Date of Birth:"
              label-align-sm="right"
              label-for="date-of-birth"
            >
              <b-form-input id="date-of-birth" type="date" v-model="contact.date_of_birth"></b-form-input>
            </b-form-group>
        </b-form-group>
        <!-- Email Addresses -->
        <hr>
        <b-form-group
          label-cols-lg="4"
          label="Email Addresses"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
        >
          <b-form-group
            v-for="(email, emailIndex) in contact.email_addresses"
            v-bind:key="emailIndex"
          >
            <b-form-group
              label-cols-sm="3"
              label="Name:"
              label-align-sm="right"
              label-for="email-name"
            >
              <b-form-input id="email-name" type="text" v-model="email.name"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Email:"
              label-align-sm="right"
              label-for="email-address"
            >
              <b-input-group prepend="@">
                <b-form-input id="email-address" type="text" v-model="email.email_address"></b-form-input>
              </b-input-group>
            </b-form-group>
            <button type="submit" class="btn btn-primary" v-on:click="deleteEmaillAddress(email)">Delete</button>
            <hr>
          </b-form-group>
          <b-form-group
              label-cols-sm="3"
              label="Name:"
              label-align-sm="right"
              label-for="email-name"
            >
              <b-form-input id="email-name" type="text" v-model="emailToAdd.name" placeholder="Add a new email address"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Email:"
              label-align-sm="right"
              label-for="email-address"
            >
              <b-input-group prepend="@">
                <b-form-input id="email-address" type="text" v-model="emailToAdd.email_address"></b-form-input>
              </b-input-group>
            </b-form-group>
            <button type="submit" class="btn btn-primary" v-on:click="addEmailAddress(emailToAdd)">Add</button>
        </b-form-group>
        <!-- Phone Numbers -->
        <hr>
        <b-form-group
          label-cols-lg="4"
          label="Phone Numbers"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-2"
        >
          <b-form-group
            v-for="(phone, phoneIndex) in contact.phone_numbers"
            v-bind:key="phoneIndex"
          >
            <b-form-group
              label-cols-sm="3"
              label="Name:"
              label-align-sm="right"
              label-for="phone-name"
            >
              <b-form-input id="phone-name" type="text" v-model="phone.name"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Name:"
              label-align-sm="right"
              label-for="phone-name"
            >
              <b-input-group prepend="#">
              <b-form-input id="phone-number" type="text" v-model="phone.phone_number"></b-form-input>
              </b-input-group>
            </b-form-group>
            <hr>
          </b-form-group>
        </b-form-group>
        <!-- Postal Addresses -->
        <hr>
        <b-form-group
          label-cols-lg="4"
          label="Postal Addresses"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-2"
        >
          <b-form-group
            v-for="(address, addressIndex) in contact.postal_addresses"
            v-bind:key="addressIndex"
          >
            <b-form-group
              label-cols-sm="3"
              label="Name:"
              label-align-sm="right"
              label-for="address-name"
            >
              <b-form-input id="address-name" type="text" v-model="address.name"></b-form-input>
            </b-form-group>
            <b-form-group
              label-cols-sm="3"
              label="Address:"
              label-align-sm="right"
              label-for="address"
            >
                <b-form-input
                readonly
                id="address"
                size="md"
                :placeholder="(address.street + ', ' + address.city + ', ' + address.state + ', ' + address.post_code + ', ' + address.country)">
              </b-form-input>
            </b-form-group>
            <hr>
          </b-form-group>
        </b-form-group>
      </b-form>
          <button type="submit" class="btn btn-primary" v-on:click="saveContact">Submit</button>
      </b-card>
    </b-container>
    </div>
</template>

<script>

import api from '@/api'

export default {
  data () {
    return {
      contact: {},
      emailToAdd: {
        name: '',
        email_address: ''
      },
      submitted: false
    }
  },
  mounted () {
    api.getContact(this.$route.params.id).then(response => {
      this.contact = response
    })
  },
  methods: {
    async saveContact () {
      if (this.contact.id) {
        await api.updateContact(this.contact.id, this.contact)
          .then(response => {
            this.$router.push('/')
          })
      }
    },
    async addEmailAddress (email) {
      api.addContactEmailAddress(this.contact.id, email)
    },
    async deleteEmaillAddress (email) {
      api.deleteContactEmailAddress(this.contact.id, email.id)
    }
  }
}
</script>
