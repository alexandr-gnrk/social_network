<template>
	<div class="login">
	    <h1>Change your password</h1>
	    <p>Using the following form:</p>
	    <v-alert v-if="message" type="error">
	      {{ message.detail }}
	    </v-alert>
	    <v-alert v-if="alert" type="success">
        {{ alert }}
	    </v-alert>
	    <form @submit.prevent="changePassword">
	        <v-text-field
	          type="password"
	          label="Old password"
	          :rules="rules"
	          hide-details="auto"
	          v-model="user.old_password"
	          required
	        ></v-text-field>
	        <v-text-field
	          type="password"
	          label="New password"
	          :rules="rules"
	          hide-details="auto"
	          v-model="user.new_password"
	          required
	        ></v-text-field>
	        <v-btn class="btn" type="submit" depressed color="primary">Change password</v-btn>
	    </form>
	</div>
</template>

<script>
export default {
	name: 'ChangePassword',
	data(){
		return {
			user: {
				'old_password': '',
				'new_password': '',
        'token': localStorage.getItem('token') || null,
			},
			message: '',
			alert: this.$store.state.alertMessage,
			rules: [
		        value => !!value || 'Required.',
		    ]
		}
	},
	methods: {
		async changePassword(){
			let requestOptions = {
				method: "PUT",
				headers: {
					'Content-Type': 'application/json',
          'dataType': 'json',
          contentType: 'json',
				},
				body: JSON.stringify(this.user)
			}

			let response = await fetch('http://127.0.0.1:8000/api/change-password/', requestOptions);
			console.log(response);
      if (await response.status === 200) {
        this.$store.state.alertMessage = "You have change your password successfully!";
				let logInBtn 		= document.querySelector('#login'),
					signUp   			= document.querySelector('#signup'),
					logOutBtn 		= document.querySelector('#logout');
				logInBtn.style.display 		= 'none';
				signUp.style.display 		  = 'none';
				logOutBtn.style.display 	= 'block';
				this.$router.push('/');
			} else if (await response.status === 400) {
				this.message = await response.json();
				this.user.old_password = '';
				this.user.new_password = '';
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