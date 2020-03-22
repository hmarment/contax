<template>
    <div>
    <b-container class="container-fluid mt-4">
      <b-card
        class="mb-3"
        title="Edit Contact"
        v-bind="contact"
      >
      <b-form @submit="saveContact">
        <b-form-group
            label-cols-lg="3"
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
        <b-form-group
          label-cols-lg="3"
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
              label="Email Address:"
              label-align-sm="right"
              label-for="email"
            >
              <b-form-input id="email" type="email" v-model="email.email_address"></b-form-input>
            </b-form-group>
          </b-form-group>
        </b-form-group>
        <!-- Phone Numbers -->
        <b-form-group
          label-cols-lg="3"
          label="Phone Numbers"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
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
              label="Email Address:"
              label-align-sm="right"
              label-for="email"
            >
              <b-form-input id="phone" type="text" v-model="phone.phone_number"></b-form-input>
            </b-form-group>
          </b-form-group>
        </b-form-group>
        <!-- Postal Addresses -->
        <b-form-group
          label-cols-lg="3"
          label="Postal Addresses"
          label-size="lg"
          label-class="font-weight-bold pt-0"
          class="mb-0"
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
              label="Street:"
              label-align-sm="right"
              label-for="street"
            >
              <b-form-input id="street" v-model="address.street"></b-form-input>
            </b-form-group>

            <b-form-group
              label-cols-sm="3"
              label="City:"
              label-align-sm="right"
              label-for="city"
            >
              <b-form-input id="city" v-model="address.city"></b-form-input>
            </b-form-group>

            <b-form-group
              label-cols-sm="3"
              label="Postcode:"
              label-align-sm="right"
              label-for="postcode"
            >
              <b-form-input id="postcode" v-model="address.post_code"></b-form-input>
            </b-form-group>

            <b-form-group
              label-cols-sm="3"
              label="State:"
              label-align-sm="right"
              label-for="state"
            >
              <b-form-input id="state" v-model="address.state"></b-form-input>
            </b-form-group>

            <b-form-group
              label-cols-sm="3"
              label="Country:"
              label-align-sm="right"
              label-for="country"
            >
              <b-form-input id="country" v-model="address.country"></b-form-input>
            </b-form-group>
          </b-form-group>
        </b-form-group>
      </b-form>
            <button type="submit" class="btn btn-primary" v-on:click="saveContact">Submit</button>
        <!-- </form> -->
      </b-card>
    </b-container>
    </div>
</template>

<script>

import api from '@/api'

export default {
  data () {
    return {
      contact: {
        first_name: '',
        last_name: ''
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
    update: function (e) {
      this.$validator.validate().then(result => {
        this.submitted = true
        if (!result) {
          return
        }
        api.updateContact(this.contact)
          .then(response => {
            this.$router.push('/')
          })
      })
    },
    async saveContact () {
      if (this.contact.id) {
        await api.updateContact(this.contact.id, this.contact)
          .then(response => {
            this.$router.push('/')
          })
      }
    }
  }
}
</script>
