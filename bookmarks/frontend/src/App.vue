<template>
  <div id="app">
    <v-app id="main">
      <Navbar />
      <v-main>
        <v-container fluid my-10>
          <!-- If using vue-router -->
          <router-view></router-view>
        </v-container>
      </v-main>
      <Footer />
    </v-app>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default {
  name: "App",
  data() {
    return {
      alert: this.$store.state.alertMessage,
    };
  },
  components: {
    Navbar, Footer
  },
};
</script>

