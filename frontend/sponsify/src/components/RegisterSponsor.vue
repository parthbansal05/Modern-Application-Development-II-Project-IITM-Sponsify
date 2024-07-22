<template>
	<div>
		<form @submit.prevent="register">
			<input v-model="username" placeholder="Username" type="text" required />
			<input v-model="email" placeholder="Email" type="email" required />
			<input v-model="password" type="password" placeholder="Password" required />
			<input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
			<input v-model="phno" type="text" placeholder="Phone Number" required />

			<select v-model="industry" required>
				<option value="Food & Beverage">Food & Beverage</option>
				<option value="Health & Wellness">Health & Wellness</option>
				<option value="Fashion & Apparel">Fashion & Apparel</option>
				<option value="Travel & Hospitality">Travel & Hospitality</option>
				<option value="Technology & Electronics">Technology & Electronics</option>
				<option value="Education">Education</option>
				<option value="Lifestyle">Lifestyle</option>
				<option value="Gaming & Esports">Gaming & Esports</option>
				<option value="Beauty & Personal Care">Beauty & Personal Care</option>
				<option value="Finance & Banking">Finance & Banking</option>
				<option value="Parenting & Family">Parenting & Family</option>
				<option value="Entertainment">Entertainment</option>
				<option value="Music">Music</option>
				<option value="Sports & Fitness">Sports & Fitness</option>
				<option value="Automotive">Automotive</option>
				<option value="Real Estate">Real Estate</option>
				<option value="Home & Garden">Home & Garden</option>
				<option value="Pet Care">Pet Care</option>
				<option value="Sustainability & Environment">Sustainability & Environment</option>
				<option value="Non-profit & Charity">Non-profit & Charity</option>
			</select>

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
			industry: 'Food & Beverage',
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
				await axios.post('http://localhost:5000/sponsor/register', {
					username: this.username,
					email: this.email,
					pwd: this.password,
					phno: this.phno,
					industry: this.industry,
					next: this.$route.query.next
				});
				this.msg = 'Sponsor registered successfully';
			} catch (err) {
				this.error = 'Error registering Sponsor';
			}
		}
	}
};
</script>