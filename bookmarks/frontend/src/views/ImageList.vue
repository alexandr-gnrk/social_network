<template>
  <div>
    <v-row>
      <!-- <v-card
        v-for="image in images" :key="image.id"
        class="my-5 mx-auto"
        max-width="400"
      >
        <v-img
          class="white--text align-end"
          height="200px"
          :src="image.image"
          :alt="image.title"
        >
        </v-img>
        <v-card-subtitle class="pb-0">
          {{ image.title }}
        </v-card-subtitle>
        <v-card-text class="text--primary" v-if="isExplore">
          <div>{{ image.description }}</div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="orange" text>Share</v-btn>
          <v-btn color="orange" text @click="isExplore = !isExplore">Explore</v-btn>
          <router-link :to="{ name: 'image-detail', params: { id: image.id } }">
            <v-btn color="orange" text>Detail</v-btn>
          </router-link>
        </v-card-actions>
      </v-card> -->

      <ImageCard
        v-for="image in images" :key="image.id"
        :id="image.id"
        :title="image.title"
        :description="image.description"
        :img="image.image"
        :isExplore="isExplore"
        @open-description="openDescription"
       />
      <!-- <image-card></image-card> -->
    </v-row>
  </div>
</template>

<script>
import ImageCard from '../components/ImageCard.vue';

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
      isExplore: false,
    }
  },
  methods: {
    async loadImages () {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          "Authorization": "JWT " + token,
        },
      }
      var response = await fetch('http://localhost:8000/images/api/', requestOptions);
      this.images = await response.json();
    },
    openDescription() {
      console.log('Hello from component')
    },
  },
  created () {
    this.loadImages()
  },
  components: {
    // 'image-card': ImageCard,
    ImageCard,
  }
}
</script>
