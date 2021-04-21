<template>
	<div class="logout">
		<h1>You have successfully logged out.</h1>
	</div>
</template>

<script>
	export default{
		name: 'Logout',
		created(){
			localStorage.removeItem('token');
      localStorage.removeItem('user');
      let logInBtn       = document.querySelector('#login'),
          signUpBtn      = document.querySelector('#signup'),
          logOutBtn      = document.querySelector('#logout');
        logInBtn.style.display    = 'block';
        signUpBtn.style.display   = 'block';
        logOutBtn.style.display   = 'none';
		}
	}
</script>

<style>
  .logout{
    padding: 50px;
  }

  .logout h1{
    text-align: center;
    margin-bottom: 10px;
  }

  .logout p{
  	text-align: center;
  }
</style>