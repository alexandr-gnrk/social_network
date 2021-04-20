<template>
    <v-alert
      v-if="alert"
      class="my-2"
      dense
      text
      :color="alert.color"
      :type="alert.type"
      @click="$emit('close')"
    >
      {{ alert.text }}
    </v-alert>
</template>

<script>

export default {
  // props: {
  //   alert: {
  //     color: {
  //       type: String,
  //       required: false,
  //       default: null
  //     },
  //     type: {
  //       type: String,
  //       required: false,
  //       default: 'success',
  //       validator(value) {
  //         return ['success', 'info', 'warning', 'error'].includes(value)
  //       }
  //     },
  //     text: String
  //   }
  // },

  props: ['alert'],
  emits: ['close']
}
</script>
