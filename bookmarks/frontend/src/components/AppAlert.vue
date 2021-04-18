<template>
    <v-alert
      v-if="alert"
      class="my-2"
      dense
      text
      :type="alert.type"
      @click="$emit('close')"
    >
      {{ alert.title }}
      {{ alert.text }}
    </v-alert>
</template>

<script>

export default {
  props: ['alert'],
  emits: ['close']
}
</script>
