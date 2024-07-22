<template>
	<div>
		<form @submit.prevent="register">
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
		<div v-if="error">{{ error }}</div>
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
			confirmPassword: '',
			phno: '',
			category: 'Select Category',
			niche: 'Select Niche',
			error: ''
		};
	},
	methods: {
		async register() {
			try {
				const response = await axios.post('http://localhost:5000/registerInfluencer', {
					username: this.username,
					email: this.email,
					pwd: this.password,
					confirmPwd: this.confirmPassword,
					phno: this.phno,
					category: this.category,
					niche: this.niche,
					next: this.$route.query.next
				});
			} catch (err) {
				this.error = 'Error registering influencer';
			}
		}
	}
};
</script>