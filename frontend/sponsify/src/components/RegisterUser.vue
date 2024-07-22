<template>
	<div>
		<form @submit.prevent="register">
			<input v-model="username" placeholder="Username" type="text" required />
			<input v-model="email" placeholder="Email" type="email" required />
			<input v-model="password" type="password" placeholder="Password" required />
			<input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
			<input v-model="phno" type="text" placeholder="Phone Number" required />
			<button type="submit">Register</button>
		</form>
		<div v-if="error">{{ error }}</div>
		<div v-if="msg">{{ msg }}</div>
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
				await axios.post('http://localhost:5000/user/register', {
					username: this.username,
					email: this.email,
					pwd: this.password,
					phno: this.phno,
					next: this.$route.query.next
				});
				this.msg = 'User registered successfully';
			} catch (err) {
				this.error = 'Error registering User';
			}
		}
	}
};
</script>