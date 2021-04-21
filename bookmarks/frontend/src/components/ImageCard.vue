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
      <v-btn color="orange" text @click="open">
        {{ isCardExplore ? 'Hide' : 'Explore'}}
      </v-btn>
      <v-btn color="orange" text @click="$router.push({ name: 'image-detail', params: { id: id } })">Detail</v-btn>
      <v-spacer></v-spacer>
      <v-btn color="orange" text @click="$emit('delete', id)">
        <v-icon :color="color">mdi-trash-can-outline</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>

export default {
  name: 'ImageCard',
  // props: ['title', 'description', 'img', 'id'],
  // emits: ['open-description'],
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
  emits: {
    'open-description': null,  // no validation
    'delete': null
  },
  data() {
    return {
      isCardExplore: this.isExplore // copy isExplore before use it in children
    }
  },
  methods: {
    open() {
      this.isCardExplore = !this.isCardExplore
      if (this.isCardExplore) {
        this.$emit('open-description') // send event on top to parent
      }
    },
  },
}
</script>

