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
      
      <v-card-text class="text--primary" v-if="image.users_like.length === 0">
        Nobody likes this image yet.
      </v-card-text>

      <v-card-actions p-10>
        <v-spacer></v-spacer>
        <LikeImageButton
          :id="id"
          :action="action"
          @like-image="likeImage"
         />
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

    <v-card
      v-if="image.users_like.length > 0"
      class="mx-auto mt-10"
      width="1000"
    >
      <v-row class="pa-3">
        <v-card
          class="ml-5"
          max-width="300"
          v-for="person in image.users_like"
          :key="person"
          flat
        >
          <v-img
            :src="'http://127.0.0.1:8000' + person.profile.photo"
            aspect-ratio="1"
            class="grey lighten-2 rounded-circle"
            width="100px"
          ></v-img>
          <v-card-subtitle class="pb-0 mx-auto">
            {{ person.profile.user }}
          </v-card-subtitle>
        </v-card>
      </v-row>
    </v-card>

  </div>
</template>


<script>
import LikeImageButton from '../components/LikeImageButton.vue';

export default {
  name: 'ImageDetail',
  data() {
    return {
      id: parseInt(this.$route.params.id),
      user: localStorage.getItem('user'),
      apiUrl: 'http://127.0.0.1:8000',
      image: {},
    }
  },
  computed: {
    action() {
      if (this.image.users_like.includes(this.user)) {
        return this.action = 'dislike'
      }
      return this.action = 'like'
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
      var response = await fetch('http://localhost:8000/images/api/' + this.id, requestOptions);
      this.image = await response.json();
    },
    likeImage() {
      this.loadImage()
    },
  },
  components: {
    LikeImageButton
  }
}
</script>

