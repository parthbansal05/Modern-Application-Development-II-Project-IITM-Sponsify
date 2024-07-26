<template>
	<div class="register-container">
		<div v-if="error" class = "error-message">
			{{ error }}

			<button @click="closeError" class="err-close-btn">
				&nbsp; &times; &nbsp;
			</button>

		</div>

		<div v-if="msg" class = "success-message">
			{{ msg }}

			<button @click="closeMsg" class="msg-close-btn">
				&nbsp; &times; &nbsp;
			</button>

		</div>

		<form @submit.prevent="register" class="register-form">
			<input v-model="username" placeholder="Username" type="text" required />
			<input v-model="email" placeholder="Email" type="email" required />
			<input v-model="password" type="password" placeholder="Password" required />
			<input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
			<input v-model="phno" type="text" placeholder="Phone Number" required />
			<button type="submit">Register</button>
		</form>
		
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			username: '',
			email: '',
			password: '',
			phno: '',
			error: '',
			msg: ''
		};
	},
	methods: {
		async register() {
			try {
				// check if the password and confirm password match
				this.error = '';
				this.msg = '';
				if (this.password !== this.confirmPassword) {
					this.error = 'Passwords do not match';
					return;
				}
				const response = await axios.post('http://localhost:5000/user/register', {
					username: this.username,
					email: this.email,
					pwd: this.password,
					phno: this.phno,
					next: this.$route.query.next
				});
				if ('error' in response.data) {
                    this.error = response.data.error;
                    return;
                }
				if ('msg' in response.data) {
                    this.msg = response.data.msg;
                    return;
                }
			} catch (err) {
				this.error = 'Error registering User';
			}
		},

		closeError() {
			this.error = null
		},

		closeMsg() {
			this.msg = null
		}
	}
};
</script>


<style scoped>

.error-message{
	display: flex;
	width: 50rem;
	align-items: center;
	justify-content: space-between;
	font-size: 1.2rem;
	background: rgba(255, 107, 107, 0.8);
	color: rgb(188, 0, 0);
	padding: 1rem;
	border-radius: 8px;
	margin-bottom: 8px;
}
.err-close-btn{
	position: relative;
	top: 0px;
	right: 0px;
	background: none;
	border: none;
	border-radius: 2px; 
	font-size: 2rem;
	cursor: pointer;
	color: rgb(188, 0, 0);
	padding: 0rem; 
}
.err-close-btn:hover {
	color: darkred;
}

.success-message{
	display: flex;
	width: 50rem;
	align-items: center;
	justify-content: space-between;
	font-size: 1.2rem;
	background: rgba(144, 238, 144, 0.8); /* light green */
	color: green;
	padding: 1rem;
	border-radius: 8px;
	margin-bottom: 8px;
}
.msg-close-btn{
	position: relative;
	top: 0px;
	right: 0px;
	background: none;
	border: none;
	border-radius: 2px; 
	font-size: 2rem;
	cursor: pointer;
	color: green;
	padding: 0rem; 
}
.msg-close-btn:hover {
	color: darkgreen;
}

.register-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 100vh;
	background-color: #FFFFFF;
	background-image: url('@/assets/background.jpeg'); /* Replace with your image path */
	background-size: cover; /* Adjust this to cover, contain, or other values based on your need */
	background-position: center; /* Adjust the position as needed */
	background-repeat: no-repeat; /* Ensure the image doesn't repeat */
}	

.register-form {
    display: flex;
    width: 50rem;
    flex-direction: column;
    background: white;
    padding: 1.5rem;
    padding-right: 25rem;
    border-radius: 8px;

    
    position: relative;
    z-index: 2;
    
    background: linear-gradient(to right, rgba(255, 255, 255, 0.9) 50%, rgba(255, 255, 255, 0.3) 55%,rgba(255, 255, 255, 0) 60%),url('@/assets/leafy_bg.jpeg');
    background-size: cover;
}

.register-form input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    font-size: 1rem;
    background-color: #FFFFFF;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.register-form button {
    padding: 0.5rem;
    font-size: 1rem;
    color: white;
    background-color: #38566E;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.register-form select {
    margin-bottom: 1rem;
    padding: 0.5rem;
    font-size: 1rem;
    background-color: #FFFFFF;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.register-form button:hover {
    background-color: #B97A57;
}


</style>