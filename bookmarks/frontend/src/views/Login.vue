<template>
	<div class="login">
	    <h1>Log in</h1>
	    <p>Please, log in using the following form:</p>
	    <v-alert v-if="message" type="error">
	      {{ message.detail }}
	    </v-alert>
	    <v-alert v-if="alert" type="success">
	        {{ alert }}
	    </v-alert>
	    <form @submit.prevent="loginUser">
	        <v-text-field
	          label="Username or email"
	          :rules="rules"
	          hide-details="auto"
	          v-model="user.username"
	          required
	        ></v-text-field>
	        <v-text-field
	          type="password"
	          label="Password"
	          :rules="rules"
	          hide-details="auto"
	          v-model="user.password"
	          required
	        ></v-text-field>
	        <v-btn class="btn" type="submit" depressed color="primary">Log in</v-btn>
	    </form>
	    <p>Are you a member yet? <router-link to="register">Sign up</router-link></p>
	</div>
</template>

<script>
export default{
	name: 'Login',
	data(){
		return {
			user: {
				'username': '',
				'password': ''
			},
			message: '',
			alert: this.$store.state.alertMessage,
			rules: [
		        value => !!value || 'Required.',
		        value => (value && value.length >= 3) || 'Min 3 characters',
		    ]
		}
	},
	created(){
		setTimeout(function(){
			this.$store.state.alertMessage = '';
		}, 4000);
	},
	methods: {
		async loginUser(){
			let requestOptions = {
				method: "POST",
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(this.user)
			}

			let response = await fetch('http://localhost:8000/api/auth/', requestOptions);
			if(await response.status === 200){
				this.message = await response.json();
				localStorage.setItem('token', this.message.token);
				localStorage.setItem('user', this.message.user);
				let logInBtn 		= document.querySelector('#login'),
					signUp 			= document.querySelector('#signup'),
					logOutBtn 		= document.querySelector('#logout');
				logInBtn.style.display 		= 'none';
				signUp.style.display 		= 'none';
				logOutBtn.style.display 	= 'block';
				this.$router.push('/');
			}else if(await response.status === 400){
				this.message = await response.json();
				this.user.username = '';
				this.user.password = '';
			}
		}
	}
}
</script>

<style>
  .login{
    width: 600px;
    margin: 0 auto;
    padding: 50px 0;
  }

  .btn{
    margin: 10px 0;
  }
</style>