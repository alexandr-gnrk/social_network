<template>
    <v-list>
      <v-list-item>
        <v-list-item-avatar
          size="200"
          class="mx-auto"
        >
          <v-img
            :src="photo"
          ></v-img>
        </v-list-item-avatar>
      </v-list-item>
      <v-list-item link
       router-link :to = "{ name: 'user-detail', params: { id: id } }"
      >
        <v-list-item-content>
          <v-list-item-title class="title green--text">
            {{ username }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
</template>


<script>

export default {
  name: 'UserCard',
  props: {
    photo: String,
    username: String,
    stripe_id: String,
    id: Number
  },
}
</script>
