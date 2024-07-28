<template>
	<html>
		<img src="@/assets/sponsify_logo_black.png" alt="Logo" class="logo-img">
		
		<body>
			<br><br><br><br><br>
		<h1>
			404
		</h1>
		<h3><ins>Page Not Found</ins></h3>
		
		<p>
			<ins></ins>

			<code>The page you are looking for does not exist.</code> 
			<br><br><br><br><br><br>
			<router-link to="/" class="home-btn">Go to Login Page</router-link>
		
		</p>
	</body>

	</html>
</template>

<script>
export default {
	name: 'NotFound'
}
</script>

<style scoped>
* {
	margin: 0;
	padding: 0
}

html,
code {
	font: 15px/22px arial, sans-serif
}

html {
	background: #fff;
	color: #222;
	padding: 15px
}

body {
	margin: 7% auto 0;
	width: 780px;
	height: 560px;
	padding: 30px 0 15px
}

*>body {
	background: url(//www.google.com/images/errors/robot.png) 100% 5px no-repeat;
	background-size: 40%;
	padding-right: 205px
}

p {
	margin: 11px 0 22px;
	overflow: hidden
}

ins {
	color: #777;
	text-decoration: none
}

a img {
	border: 0
}

@media screen and (max-width:772px) {
	body {
		background: none;
		margin-top: 0;
		max-width: none;
		padding-right: 0
	}
}

.b {
	font-size: 40px;
}



.logo-img{
	position: absolute;
	top: 120px;
	left: 390px;
	width: auto;
	height: 100px;
}
</style>