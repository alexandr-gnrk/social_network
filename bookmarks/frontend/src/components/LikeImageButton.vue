<template>
  <v-btn icon @click="likeImage">
    <v-icon :color="color">mdi-heart</v-icon>
  </v-btn>
</template>


<script>

export default {
  name: 'LikeButton',
  props: {
    id: Number,
    action: String
  },
  emits: {
    'like-image': null
  },
  computed: {
    color() {
      return this.action === 'like' ? 'grey' : 'orange'
    }
  },
  methods: {
    async likeImage () {
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
      await fetch('http://localhost:8000/images/api-like/', requestOptions);
      this.$emit('like-image')
    },
  }
}
</script>
