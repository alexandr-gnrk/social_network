<template>
  <div>
    <v-card
      class="mx-auto"
      width="1000"
    >
      <v-img
        class="white--text align-end"
        :src="apiUrl + image.image"
        :alt="image.title"
      >
        <v-card-title>
          {{ image.title }}
        </v-card-title>
      </v-img>
      <v-card-text class="text--primary">
        <div>{{ image.description }}</div>
      </v-card-text>

      <v-card-text class="text--primary">
        Users like: 
        <span v-for="user in image.users_like" :key="user">{{ user }} </span>
      </v-card-text>

      <v-card-actions p-10>
        <v-spacer></v-spacer>

        <v-btn icon @click="isLike = !isLike">
          <v-icon :style="{color: isLike ? 'orange' : 'grey'}">mdi-heart</v-icon>
        </v-btn>

        <v-btn icon @click="likeImage">
          <v-icon style="color:orange">mdi-heart</v-icon>
        </v-btn>
        <span class="grey--text">
          {{ image.total_likes }}
        </span>

        <v-btn icon>
          <v-icon>mdi-eye</v-icon>
        </v-btn>
        <span class="grey--text">
          {{ image.total_views }}
        </span>

      </v-card-actions>

    </v-card>
  </div>
</template>


<script>

export default {
  name: 'ImageDetail',
  data() {
    return {
      isLike: false,
      like: {
        id: '',
        action: ''
      },
      image: {},
      apiUrl: 'http://127.0.0.1:8000'
    }
  },
  created () {
    this.loadImage()
  },
  methods: {
    async loadImage () {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        }
      };
      var response = await fetch('http://localhost:8000/images/api/' + this.$route.params.id, requestOptions);
      this.image = await response.json();
    },
    async likeImage () {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        },
        body: JSON.stringify({
          'id': this.$route.params.id,
          'action': 'like'
        }),
      };
      var response = await fetch('http://localhost:8000/images/api-like/', requestOptions);
      this.like = await response.json();
      console.log(this.like)
      this.loadImage
    },
  } 
}
</script>

