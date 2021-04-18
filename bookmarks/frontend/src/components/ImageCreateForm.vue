<template>
  <div class="grey lighten-4 mx-5">
      <h3>Add image</h3>  
      <v-form @submit.prevent="createImage">
        <v-text-field
          v-model.trim="image.title"
          label="Title"
          required
        ></v-text-field>
        <v-alert
          v-if="errors.title"
          color="red lighten-2"
          type="info"
        >
          {{ errors.title }}
        </v-alert>
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
        <v-btn type="submit" class="mr-4" color="success">Create image</v-btn>
      </v-form>
      <v-alert
        v-if="alert"
        class="mt-5"
        dense
        text
        type="success"
      >
        {{ alert.title }}
        {{ alert.text }}
      </v-alert>
  </div>
</template>


<script>

export default {
  name: "ImageCreateForm",
  emits: ['create-image'],
  data() {
    return {
      image: {
        title: '',
        description: '',
        url: '',
      },
      errors: {
        title: null
      },
      alert: null
    }
  },
  methods: {
    async createImage() {
      if (this.formIsValid()) {
        let token = localStorage.getItem('token');
        let requestOptions = {
          method: 'POST',
          headers: {
            "Content-type": 'application/json',
            "Authorization": "JWT " + token,
          },
          body: JSON.stringify(this.image)
        };
        await fetch("http://127.0.0.1:8000/images/api-create/", requestOptions);
        this.$emit('create-image');
        this.image = {}
        this.alert = {
          title: 'Success!',
          text: `Image was created`
        }
      }
    },
    formIsValid() {
      let isValid = true
      if (this.image.title.length === 0) {
        this.errors.title = "Image title can't be empty"
        isValid = false
      } else {
        this.errors.title = null
      }
      return isValid
    }
  }
}
</script>