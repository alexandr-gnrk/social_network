<template>
  <div class="m-5">
    <v-row class="m-5">
      <v-card
        v-for="image in images" :key="image.id"
        class="mx-auto"
        max-width="400"
      >
        <v-img
          class="white--text align-end"
          height="200px"
          src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        >
        </v-img>
        <v-card-subtitle class="pb-0">
          {{ image.title }}
        </v-card-subtitle>
        <v-card-text class="text--primary">
          <div>{{ image.description }}</div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="orange" text>Share</v-btn>
          <v-btn color="orange" text>Explore</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </div>

</template>

<script>

export default {
  name: 'ImageRanking',
  data() {
    return {
      images: []
    }
  },
  async created () {
    let token = localStorage.getItem('token');
    let requestOptions = {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        "Authorization": "JWT " + token,
      },
    }
    var response = await fetch('http://localhost:8000/images/api-ranking/', requestOptions);
    this.images = await response.json();
  },
}
</script>
