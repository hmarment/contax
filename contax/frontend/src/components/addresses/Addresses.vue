<template>
  <div>
    <b-container class="container-fluid mt-4">
      <b-card-group deck v-for="(address_group, count) in addresses" v-bind:key="count">
        <b-card v-for="address in address_group" v-bind:key="address.id"
          style="max-width: 22rem;"
          class="mb-3"
        >
            <b-card-title>{{ address.street}}</b-card-title>
            <b-card-text>
                {{ address.street }}
                <br>
                {{ address.city }}
                <br>
                {{ address.post_code }}
                <br>
                {{ address.state }}
                <br>
                {{ address.country }}
            </b-card-text>
            <!-- <b-card-sub-title class="mb-2"> </b-card-sub-title> -->
            <b-list-group flush v-if="address.contacts.length > 0">
              <br>
              <span><b>Contacts</b></span>
              <b-list-group-item v-for="(contact, contactIndex) in address.contacts" v-bind:key="contactIndex">{{ contact.first_name }} {{ contact.last_name }}</b-list-group-item>
            </b-list-group>
          <br>
          <b-button :href="('#/addresses/edit/' + address.id)" variant="primary">Edit</b-button>
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
      addresses: [],
      model: {}
    }
  },
  async created () {
    this.refreshAddresses()
  },
  methods: {
    async refreshAddresses () {
      this.loading = true
      var addresses = await api.getAddresses()
      var i
      var j
      var chunkedAddresses = []
      var chunkSize = 3
      for (i = 0, j = addresses.length; i < j; i += chunkSize) {
        chunkedAddresses.push(addresses.slice(i, i + chunkSize))
      }
      this.addresses = chunkedAddresses
      this.loading = false
    }
  }
}
</script>
