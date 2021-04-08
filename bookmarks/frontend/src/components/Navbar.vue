<template>
  <v-app-bar app flat color="green">
    <v-toolbar-title class="title">
      <router-link to="/" class="link"><span>Social network</span></router-link>
    </v-toolbar-title>
    <v-btn text>
      <router-link :to = "{ name:'dashboard' }" class="link"><span>My dashboard</span></router-link>
    </v-btn>
    <v-btn text>
      <router-link :to = "{ name:'image-list' }" class="link"><span>Images</span></router-link>
    </v-btn>
    <v-btn text>
      <router-link :to = "{ name:'image-ranking' }" class="link"><span>Image ranking</span></router-link>
    </v-btn>				
    <v-btn text>
      <router-link :to = "{ name:'people' }" class="link"><span>People</span></router-link>
    </v-btn>
    <v-btn text>
      <router-link :to = "{ name:'notifications' }" class="link"><span>Send mail</span></router-link>
    </v-btn>
    <v-btn text>
      <router-link :to = "{ name:'image-create' }" class="link"><span>Bookmarklet</span></router-link>
    </v-btn>

    <v-spacer></v-spacer>

    <div v-if="user">
      <v-p style="color:yellow">Hello, {{ user }}</v-p>
      <router-link :to = "{ name:'logout' }" class="link ml-5"><span>Logout</span></router-link>
    </div>
    <div v-else>
      <router-link :to = "{ name:'login' }" class="link"><span>Login</span></router-link>
      <router-link :to = "{ name:'register' }" class="link ml-5"><span>Signup</span></router-link>
    </div>
  </v-app-bar>
</template>


<script>
  export default {
    name: "Navbar",
    data() {
    	return {
    		user: localStorage.getItem('user')
    	}
    }
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
		color:white;
	}
	.link .login{
		color: blue;
	}
	.title{
		margin-right: 100px;
	}
</style>
