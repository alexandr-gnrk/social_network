<template>
	<div id="app">
		<v-app id="main">
      <Navbar />>
		  <v-main>
			  <router-view></router-view>
			</v-main>

			<v-footer padless> 
				<v-col class="text-center" cols="12">
				  2021 - {{ new Date().getFullYear() }} — <strong>Social network</strong>
				</v-col>
			</v-footer>
  		</v-app>
	</div>
</template>

<script>

import Navbar from '@/components/Navbar'

export default {
  name: 'App',
  data(){
    return {
      alert: this.$store.state.alertMessage
    }
  },
  components: {
    Navbar
  },
}
</script>

