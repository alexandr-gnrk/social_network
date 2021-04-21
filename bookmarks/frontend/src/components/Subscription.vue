<template>
  <v-card
    class="grey lighten-4 pa-2 my-5"
    flat
    tile
    min-width="200"
  >
    <v-btn class="mr-2 green" dark @click="createCheckoutSession">
      <v-icon>mdi-credit-card-outline</v-icon>
      <span>Subscribe</span>
    </v-btn>
    <v-btn class="mr-2 blue" dark @click="createCustomerPortalSession">
      <v-icon>mdi-credit-card-refresh-outline</v-icon>
      <span>Manage billing</span>
    </v-btn>
  </v-card>
</template>


<script>

export default {
  name: 'Subscription',
  data() {
    return {
    }
  },
  methods: {
    async createCheckoutSession() {
      var stripe = Stripe("pk_test_51IXqAwIBBCpvms2A0tZdmSSd78uaVKdZ86iOhZrbKAxO4uf41sgvHWyp6q71h11shWh0ZNFR1BLZBnzmgzSKWd8a00T1RT6ZMQ");
      let token = localStorage.getItem('token');
      await fetch("http://localhost:8000/sub/api/create-checkout-session/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        }
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then(function (result) {
          if (result.error) {
            alert(result.error.message);
          }
        })
        .catch(function (error) {
          console.error("Error:", error);
        });
    },
    async createCustomerPortalSession() {
      let token = localStorage.getItem('token');
      await fetch("http://localhost:8000/sub/api/create-customer-portal-session/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "JWT " + token,
        },
      })
        .then(function(response) {
          return response.json()
        })
        .then(function(data) {
          window.location.href = data.url;
        })
        .catch(function(error) {
          console.error('Error:', error);
        });
    },
  }
}
</script>
