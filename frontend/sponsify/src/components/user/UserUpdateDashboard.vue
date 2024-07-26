<template>
	<div>
		{{ email }}
		{{ username }}
		{{ ph_no }}
		<form @submit.prevent="updateUserDashboard">
			<input v-model="email" :placeholder="email" type="email" />
			<input v-model="password" type="password" placeholder="Password" required />
			<input v-model="username" :placeholder="username" type="text" required />
			<input v-model="ph_no" :placeholder="ph_no" type="number" required />
			<button type="submit">Login</button>
		</form>
		<div v-if="error">{{ error }}</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			email: '',
			username: '',
			ph_no: ''
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/user/update_dashboard', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.email = response.data.email;
			this.username = response.data.username;
			this.ph_no = response.data.ph_no;
		} catch (err) {
			console.log(err);
		}
	},
	methods: {
		async updateUserDashboard() {
			try {
				const response = await axios.post('http://localhost:5000/user/update_dashboard', {
					pwd: this.password,
					username: this.username,
					ph_no: this.ph_no,
					next: this.$route.query.next
				}, {
					headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
				});
				console.log(response.data);
			} catch (err) {
				this.error = 'Invalid username or password';
			}
		}
	}
};
</script>