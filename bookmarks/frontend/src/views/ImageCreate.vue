<template>
  <div class="m-5">
    <v-col cols="12" sm="4" class="grey lighten-4 mx-5">
      <h3>Bookmark an image</h3>  
      <v-form @submit.prevent="createImage">
        <v-text-field
          v-model.trim="image.title"
          label="Title"
          required
        ></v-text-field>
        <v-text-field
          v-model.trim="image.description"
          label="Description"
          required
        ></v-text-field>
        <v-text-field
          v-model.trim="image.url"
          label="Url"
          required
        ></v-text-field>
        <v-btn class="mr-4" color="success" type="submit">Create image</v-btn>
      </v-form>      
    </v-col>
  </div>
</template>


<script>

export default {
  name: "ImageCreate",
  data() {
    return {
      image: {
        title: '',
        description: '',
        url: '',
      }
    }
  },
  methods: {
    async createImage() {
      let token = localStorage.getItem('token');
      let requestOptions = {
        method: 'POST',
        headers: {
          "Content-type": 'application/json',
          "Authorization": "JWT " + token,
        },
        body: JSON.stringify(this.image)
      }
      var response = await fetch("http://127.0.0.1:8000/images/api-create/", requestOptions);
      this.image.push(await response.json());
    }
  },
}
</script>