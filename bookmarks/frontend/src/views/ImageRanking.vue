<template>
  <div>
    <v-row>
      <div
        class="mx-auto mt-5"
        v-for="image in images" :key="image.id"
      >
        <image-card
          :title="image.title"
          :description="image.description"
          :img="apiUrl + image.image"
          :id="image.id"
          @addLike="addLike(image.id)"
        />
      </div>
    </v-row>
  </div>
</template>


<script>
import ImageCard from "@/components/ImageCard";

export default {
  name: 'ImageRanking',
  components: { ImageCard },
  data() {
    return {
      images: [],
      apiUrl: 'http://127.0.0.1:8000'
    }
  },
  methods: {
    addLike(imageId) {
      console.log(imageId)
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
    var response = await fetch('http://localhost:8000/images/api/ranking/', requestOptions);
    this.images = await response.json();
    console.log(this.images)
  }
}
</script>