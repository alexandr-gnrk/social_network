<template>
  <div class="register">
    <h1>Create an account</h1>
    <p>Please, sign up using the following form:</p>
    <v-alert v-for="[msg], i in message" type="error" :key="i">
      {{ msg }}
    </v-alert>
    <form @submit.prevent="createUser">
        <v-text-field
          label="Username"
          :rules="rules"
          hide-details="auto"
          required
          v-model="user.username"
        ></v-text-field>
        <v-text-field
          label="First name"
          :rules="rules"
          hide-details="auto"
          required
          v-model="user.first_name"
        ></v-text-field>
        <v-text-field
          type="email"
          label="Email"
          :rules="rules"
          hide-details="auto"
          required
          v-model="user.email"
        ></v-text-field>
        <v-text-field
          type="password"
          label="Password"
          :rules="rules"
          hide-details="auto"
          required
          v-model="user.password"
        ></v-text-field>
        <v-text-field
          type="password"
          label="Repeat password"
          :rules="rules"
          hide-details="auto"
          required
          v-model="user.password2"
        ></v-text-field>
        <v-btn class="btn" type="submit" depressed color="primary">Sign up</v-btn>
    </form>
    <p>Already a member? <router-link to="login">Log in</router-link></p>
  </div>
</template>

<script>

export default {
  name: 'Register',
  data(){
    return {
      user: {
        'username': '',
        'first_name': '',
        'email': '',
        'password': '',
        'password2': ''
      },
      rules: [
        value => !!value || 'Required.',
        value => (value && value.length >= 3) || 'Min 3 characters',
      ],
      message: ''
    }
  },
  methods: {
    async createUser(){
      let requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.user)
      }
      let response = await fetch('http://localhost:8000/api/register/', requestOptions);
      if(await response.status === 201){
        this.$store.state.alertMessage = "You have signed up successfully! Please, log in!";
        this.$router.push('/login');
      }else if(await response.status === 400){
        this.message = await response.json();
        if(this.message.username && this.message.email){
          this.user.username = '';
          this.user.email = '';
        }else if(this.message.email){
          this.user.email = '';
        }else if(this.message.username){
          this.user.username = '';
        }else{
          this.user.password = '';
          this.user.password2 = '';
        }
      }
    }
  }
}
</script>

<style>
  .register{
    width: 600px;
    margin: 0 auto;
    padding: 50px 0;
  }

  .btn{
    margin: 10px 0;
  }

  #logout{
    display: none;
  }
</style>