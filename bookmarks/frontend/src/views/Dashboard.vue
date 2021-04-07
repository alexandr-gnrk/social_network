<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p>Welcome to your dashboard, <strong>{{ user }}</strong>. You can edit your profile or 
      <router-link :to = "{ name:'change-password' }">change your password</router-link>.</p>
    <p>For now, you have bookmarked 2 images.</p>
    <p>Drag the following button to your bookmarks toolbar to bookmark images from other websites Bookmark it</p>
    <p>You can also edit your profile or change your password.</p>
  </div>    
</template>

<script>
  export default {
    data(){
    	return{
    		user: localStorage.getItem('user')
    	}
    }
}
</script>

<style>
	.dashboard{
    padding: 50px;
  }

  .dashboard h1{
    text-align: center;
    margin-bottom: 10px;
  }
</style>