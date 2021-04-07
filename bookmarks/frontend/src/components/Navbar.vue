<template>
  <v-app-bar app>
    <v-toolbar-title class="title"><router-link to="/" class="link"><span>Social network</span></router-link></v-toolbar-title>
    <v-btn text>
      <router-link to="/" class="link"><span>My dashboard</span></router-link>
    </v-btn>
    <v-btn text>
      <router-link :to = "{ name:'image-list' }" class="link"><span>Images</span></router-link>
    </v-btn>				
    <v-btn text>
      People
    </v-btn> 
    <router-link to="/login" class="link">
      <v-btn text color="primary" id="login">Log in</v-btn>
    </router-link>     
    <router-link to="/register" class="link" id="signup">
      <v-btn text color="primary">Sign up</v-btn>          
    </router-link>
    <router-link to="/logout" class="link" id="logout">
      <v-btn text color="primary" class="logout">Log out</v-btn>
    </router-link>
  </v-app-bar>
</template>

<script>
export default {
  name: "Navbar"
}
</script>

<style>
	.menu-item{
		color: white;
	}
	.link{
		text-decoration: none;
	}
	.link span{
		text-decoration: none;
		color: #000000;
	}
	.link .login{
		color: blue;
	}
	.title{
		margin-right: 50px;
	}
</style>
