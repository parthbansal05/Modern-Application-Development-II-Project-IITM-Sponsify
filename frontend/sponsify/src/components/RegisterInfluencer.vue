<template>
	<div class="register-container">

		<div v-if="error" class="error-message">
			{{ error }}

			<button @click="closeError" class="err-close-btn">
				&nbsp; &times; &nbsp;
			</button>

		</div>

		<div v-if="msg" class="success-message">
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
			<select v-model="category" required>
				<option value="Cooking">Cooking</option>
				<option value="Fitness">Fitness</option>
				<option value="Fashion">Fashion</option>
				<option value="Travel">Travel</option>
				<option value="Tech">Tech</option>
				<option value="Education">Education</option>
				<option value="Lifestyle">Lifestyle</option>
				<option value="Gaming">Gaming</option>
				<option value="Health">Health</option>
				<option value="Beauty">Beauty</option>
				<option value="Finance">Finance</option>
				<option value="Parenting">Parenting</option>
				<option value="Entertainment">Entertainment</option>
				<option value="Music">Music</option>
				<option value="Sports">Sports</option>
			</select>
			<select v-model="niche" required>
				<option value="Grill">Grill</option>
				<option value="Baking">Baking</option>
				<option value="Vegetarian">Vegetarian</option>
				<option value="Vegan">Vegan</option>
				<option value="Culinary Arts">Culinary Arts</option>
				<option value="Yoga">Yoga</option>
				<option value="Bodybuilding">Bodybuilding</option>
				<option value="Cardio">Cardio</option>
				<option value="CrossFit">CrossFit</option>
				<option value="Pilates">Pilates</option>
				<option value="Streetwear">Streetwear</option>
				<option value="Luxury">Luxury</option>
				<option value="Sustainable Fashion">Sustainable Fashion</option>
				<option value="Vintage">Vintage</option>
				<option value="Accessories">Accessories</option>
				<option value="Backpacking">Backpacking</option>
				<option value="Luxury Travel">Luxury Travel</option>
				<option value="Adventure Travel">Adventure Travel</option>
				<option value="Cultural Tourism">Cultural Tourism</option>
				<option value="Solo Travel">Solo Travel</option>
				<option value="Gadgets">Gadgets</option>
				<option value="Software">Software</option>
				<option value="AI">AI</option>
				<option value="Gaming Tech">Gaming Tech</option>
				<option value="Smart Home">Smart Home</option>
				<option value="Online Courses">Online Courses</option>
				<option value="STEM">STEM</option>
				<option value="Language Learning">Language Learning</option>
				<option value="Personal Development">Personal Development</option>
				<option value="Educational Resources">Educational Resources</option>
				<option value="Home Decor">Home Decor</option>
				<option value="Minimalism">Minimalism</option>
				<option value="DIY">DIY</option>
				<option value="Sustainability">Sustainability</option>
				<option value="Travel Lifestyle">Travel Lifestyle</option>
				<option value="Esports">Esports</option>
				<option value="RPG">RPG</option>
				<option value="Strategy Games">Strategy Games</option>
				<option value="Mobile Games">Mobile Games</option>
				<option value="Console Gaming">Console Gaming</option>
				<option value="Nutrition">Nutrition</option>
				<option value="Mental Health">Mental Health</option>
				<option value="Holistic Health">Holistic Health</option>
				<option value="Fitness">Fitness</option>
				<option value="Chronic Illness">Chronic Illness</option>
				<option value="Skincare">Skincare</option>
				<option value="Makeup">Makeup</option>
				<option value="Haircare">Haircare</option>
				<option value="Nail Art">Nail Art</option>
				<option value="Beauty Tutorials">Beauty Tutorials</option>
				<option value="Investing">Investing</option>
				<option value="Personal Finance">Personal Finance</option>
				<option value="Real Estate">Real Estate</option>
				<option value="Cryptocurrency">Cryptocurrency</option>
				<option value="Financial Planning">Financial Planning</option>
				<option value="Baby Care">Baby Care</option>
				<option value="Parenting Tips">Parenting Tips</option>
				<option value="Child Education">Child Education</option>
				<option value="Family Activities">Family Activities</option>
				<option value="Teen Parenting">Teen Parenting</option>
				<option value="Movies">Movies</option>
				<option value="TV Shows">TV Shows</option>
				<option value="Theater">Theater</option>
				<option value="Celebrity News">Celebrity News</option>
				<option value="Stand-up Comedy">Stand-up Comedy</option>
				<option value="Indie">Indie</option>
				<option value="Rock">Rock</option>
				<option value="Pop">Pop</option>
				<option value="Classical">Classical</option>
				<option value="Music Production">Music Production</option>
				<option value="Football">Football</option>
				<option value="Basketball">Basketball</option>
				<option value="Tennis">Tennis</option>
				<option value="Running">Running</option>
				<option value="Swimming">Swimming</option>
			</select>

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
			category: 'Cooking',
			niche: 'Grill',
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
				const response = await axios.post('http://localhost:5000/influencer/register', {
					username: this.username,
					email: this.email,
					pwd: this.password,
					phno: this.phno,
					category: this.category,
					niche: this.niche,
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
				console.error(err);
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
.error-message {
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

.err-close-btn {
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

.success-message {
	display: flex;
	width: 50rem;
	align-items: center;
	justify-content: space-between;
	font-size: 1.2rem;
	background: rgba(144, 238, 144, 0.8);
	/* light green */
	color: green;
	padding: 1rem;
	border-radius: 8px;
	margin-bottom: 8px;
}

.msg-close-btn {
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

	background: linear-gradient(to right, rgba(255, 255, 255, 0.9) 50%, rgba(255, 255, 255, 0.3) 55%, rgba(255, 255, 255, 0) 60%), url('@/assets/leafy_bg.jpeg');
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