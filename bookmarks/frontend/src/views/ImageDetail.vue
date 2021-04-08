<template>
  <div class="mt-5">
    <div class="row">
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
          <v-btn
            color="orange"
            text
          >
            Share
          </v-btn>

          <v-btn
            color="orange"
            text
          >
            Explore
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'ImageList',
  data() {
    return {
      images: []
    }
  },
  methods: {
    async pre() {
      await axios
        .get('http://localhost:8000/images/api/', {})
        .then(response => {
          console.log(response);
        })
    }
  }
}
</script>


