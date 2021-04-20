<template>
  <div>

    <div class="pa-3 my-5">
      <h1 class="mb-5">Dashboard</h1>
      <p>Welcome to your dashboard, <strong>{{ person }}</strong>. You can edit your profile or 
        <router-link :to = "{ name:'change-password' }">change your password</router-link>.</p>
      <p>For now, you have bookmarked 2 images.</p>
      <p>Drag the following button to your bookmarks toolbar to bookmark images from other websites Bookmark it</p>
      <p>You can also edit your profile or change your password.</p>
    </div>

    <v-card
      class="pa-2 mx-auto"
      outlined
      tile
    >
      <v-toolbar
        color="grey lighten-2"
        dark
        tile
        flat
      >
        <v-toolbar-title>What's happening</v-toolbar-title>
      </v-toolbar>
      <v-list
        v-for="action in actions" :key="action"
      >
        <v-list-item>
          <v-list-item-avatar size="80">
            <v-img :src="apiUrl + action.user.profile.photo"></v-img>
          </v-list-item-avatar>

          <v-list-item-title v-if="action.verb === 'is following'">
            <v-list-item-avatar size="80">
              <v-img
              :src="apiUrl + action.target.profile.photo"
              ></v-img>
            </v-list-item-avatar>
            <router-link :to = "{ name: 'user-detail', params: { id: action.user.id } }" class="green--text">
              {{ action.user.username }}
            </router-link> 
            {{ action.verb }}
            <router-link :to = "{ name: 'user-detail', params: { id: action.target.id } }" class="green--text">
              {{ action.target.username }}
            </router-link> 
          </v-list-item-title>

          <v-list-item-title v-else>
            <v-list-item-avatar rounded size="80">
              <v-img
                :src="apiUrl + action.target.image"
                aspect-ratio="1"
                width="80px"
              ></v-img>
            </v-list-item-avatar>
            <router-link :to = "{ name: 'user-detail', params: { id: action.user.id } }" class="green--text">
              {{ action.user.username }}
            </router-link> 
            {{ action.verb }}
            <router-link :to = "{ name: 'image-detail', params: { id: action.target.id } }" class="green--text">
              {{ action.target.title }}
            </router-link> 
          </v-list-item-title>

        </v-list-item>
        <v-divider></v-divider>
      </v-list>
    </v-card>

  </div>  
</template>


<script>

export default {
  name: 'Dashboard',
  data() {
    return {
      person: localStorage.getItem('user'),
      apiUrl: 'http://127.0.0.1:8000',
      actions: [],
    }
  },
  methods: {
    async loadActions() {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        },
      }
      var response = await fetch('http://127.0.0.1:8000/api/dashboard/', requestOptions);
      this.actions = await response.json();
    },
  },
  created() {
    this.loadActions()
  },  
}
</script>


<style>
  a {
    text-decoration: none;
  }
</style>

