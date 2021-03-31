<template>
  <div>
    <stripe-checkout
      ref="checkoutRef"
      :pk="publishableKey"
      :session-id="sessionId"
    />
    <button @click="submit">Checkout!</button>
  </div>
</template>

<script>
import { StripeCheckout } from '@vue-stripe/vue-stripe';

export default {
  components: {
    StripeCheckout,
  },
  data () {
    this.publishableKey = 'pk_test_51IXqAwIBBCpvms2A0tZdmSSd78uaVKdZ86iOhZrbKAxO4uf41sgvHWyp6q71h11shWh0ZNFR1BLZBnzmgzSKWd8a00T1RT6ZMQ';
    return {
      loading: false,
      sessionId: 'session-id', // session id from backend
    };
  },
  methods: {
    submit () {
      // You will be redirected to Stripe's secure checkout page
      this.$refs.checkoutRef.redirectToCheckout();
    },

    async createCheckoutSession () {
      let token = localStorage.getItem('token');
      return await fetch("http://127.0.0.1:8000/sub/sub/session/", {
        method: "POST",
        headers: {
          "Content-type": 'application/json',
          "Authorization": "JWT " + token,
        }
      })
      .then(function (response) {
        return response.json();
      })
      .then(function (session) {
        return stripe.redirectToCheckout({ sessionId: session.id })
      })
      .then(function (result) {
        // If redirectToCheckout fails due to a browser or network
        // error, you should display the localized error message to your
        // customer using error.message.
        if (result.error) {
        alert(result.error.message);
        }
      })
      .catch(function (error) {
        console.error("Error:", error);
      });

    }
  }
}
</script>