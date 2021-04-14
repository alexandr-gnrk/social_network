<template>

    <v-card
      class="my-5 mx-auto"
      max-width="400"
    >
      <v-img
        class="white--text align-end"
        height="200px"
        :src="img"
        :alt="title"
      >
      </v-img>
      <v-card-subtitle class="pb-0">
        {{ title }}
      </v-card-subtitle>
      <v-card-text class="text--primary" v-if="isCardExplore">
        <div>{{ description }}</div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="orange" text @click="openDescription">
          {{ isCardExplore ? 'Hide' : 'Explore'}}
        </v-btn>
        <!-- <router-link :to="{ name: 'image-detail', params: { id: image.id } }">
          <v-btn color="orange" text>Detail</v-btn>
        </router-link> -->
        <v-btn color="orange" text @click="$router.push({ name: 'image-detail', params: { id: id } })">Detail</v-btn>
      </v-card-actions>
    </v-card>

</template>


<script>

export default {
  name: 'ImageCard',
  // props: ['title', 'description', 'img', 'id'],
  props: {
    title: {
      type: String,
      required: true
    },
    description: String,
    img: String,
    id: Number,
    isExplore: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      isCardExplore: this.isExplore // rename isExplore before use it in children
    }
  },
  methods: {
    openDescription() {
      this.isCardExplore = !this.isCardExplore
      this.$emit('open-description') // send event on top to parent
    }
  }
}
</script>

