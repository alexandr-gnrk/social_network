<template>
  <v-row>

    <v-col
      cols="2"
      class="flex-grow-0 flex-shrink-0"
    >
      <v-card
        class="pa-2"
        flat
        tile
      >
        <UserCard
          :photo="user.profile.photo"
          :username="user.username"
          :stripe_id="user.stripe_id"
          :id="user.id"
        />
        <v-list flat>
          <v-subheader>DESCRIPTION</v-subheader>
          <v-list-item-group
            color="primary"
          >
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Followers ({{ user.followers.length }})</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-icon>
                <v-icon :color="color">mdi-account-heart</v-icon>
              </v-list-item-icon>
              <v-list-item-content @click="followUser">
                <v-list-item-title v-if="action === 'follow'">Follow</v-list-item-title>
                <v-list-item-title v-else>Unfollow</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
    </v-col>   

    <v-col
      cols="1"
      style="min-width: 100px; max-width: 100%;"
      class="flex-grow-1 flex-shrink-0"
    >
      <v-card
        class="pa-2"
        flat
        tile
      >
        <v-row>
          <ImageCard
            v-for="image in images" :key="image.id"
            :id="image.id"
            :title="image.title"
            :description="image.description"
            :img="image.image"
            :isExplore="isExplore"
            @open-description="openDescription"
            @delete="deleteImage"
          />
        </v-row>
      </v-card>
    </v-col>

  </v-row>

</template>


<script>
import UserCard from '../components/UserCard.vue';

export default {
  name: 'UserDetail',
  data() {
    return {
      id: parseInt(this.$route.params.id),
      person: localStorage.getItem('user'),
      user: {},
    }
  },
  computed: {
    action() {
      if (this.user.followers.includes(this.person)) {
        return this.action = 'unfollow'
      }
      return this.action = 'follow'
    },
    color() {
      return this.action === 'follow' ? 'grey' : 'orange'
    }
  },  
  created () {
    this.loadUser()
  },
  methods: {
    async loadUser() {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        }
      };
      var response = await fetch('http://localhost:8000/api/' + this.id, requestOptions);
      this.user = await response.json();
    },
    async followUser() {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        },
        body: JSON.stringify({
          'id': this.id,
          'action': this.action
        }),        
      };
      await fetch('http://localhost:8000/api/users/follow/', requestOptions);
      this.loadUser()
    },

  },
  components: {
    UserCard
  }
}
</script>

