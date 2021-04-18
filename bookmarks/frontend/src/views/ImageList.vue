<template>

  <v-row class="mb-6">
    <v-col
      cols="12"
      sm="6"
      md="8"
    >
      <v-card
        class="pa-2"
        tile
        flat
      >
        <AppLoader
          v-if="loading"
        />

        <AppAlert
        :alert="alert"
        @close="alert = null"
        />

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

    <v-col
      cols="6"
      md="4"
    >
      <v-card
        class="pa-2 grey lighten-4 mt-4"
        outlined
        flat
        tile
      >
        <ImageCreateForm
          @create-image="loadImages"
        />  
      </v-card>
    </v-col>      
  </v-row>

</template>

<script>
import ImageCard from '../components/ImageCard.vue';
import ImageCreateForm from '../components/ImageCreateForm.vue';
import AppAlert from '../components/AppAlert.vue';
import AppLoader from '../components/AppLoader.vue';

export default {
  name: 'ImageList',
  data() {
    return {
      images: [],
      isExplore: false,
      alert: null,
      loading: false
    }
  },
  methods: {
    async loadImages () {
      this.loading = true // start loading
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
      this.loading = false // end loading
    },
    async deleteImage(id) {
      try {
        const title = this.images.find(image => image.id === id).title // alert.title
        let token = localStorage.getItem('token');
        let requestOptions = {
          method: "DELETE",
          headers: {
            'Content-Type': 'application/json',
            "Authorization": "JWT " + token,
          }
        };
        await fetch(`http://localhost:8000/images/api/${id}`, requestOptions);
        this.images = this.images.filter(image => image.id !== id)
        this.alert = {
          type: 'success',
          text: `Image "${title}" was deleted`,
        }
      } catch (e) {}
    },
    openDescription() {
      console.log('Hello from component')
    },
  },
  mounted () {
    this.loadImages()
  },
  components: {
    // 'image-card': ImageCard,
    ImageCard, ImageCreateForm, AppAlert, AppLoader
  }
}
</script>
