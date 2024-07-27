<template>
	<div>
		<!-- Nav and Side Bar -->
		<header class="header-bar">
			<div class="header-content">
				<button class="openbtn" @click="toggle()">
					☰
				</button>
				<img src="@/assets/sponsify_logo.png" alt="Logo" class="logo-img">
				<button @click="logout" class="logout-button">
					Logout
				</button>
			</div>
		</header>

		<div id="mySidebar" class="sidebar">
			<h3 class="sidebar-heading">Person</h3>
			<h6 class="sidebar-subheading">Post</h6>

			<div class="sidebar-buttons-top">
				<hr class="bg-white">
				<button @click="navigate('dashboard')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="navigate('view-campaigns')" class="sidebar-button btn btn-secondary btn-block mb-2">View
					Campaigns</button>
				<button @click="navigate('view-insights')" class="sidebar-button btn btn-secondary btn-block mb-2">View
					Insights</button>
			</div>

			<div class="sidebar-buttons-bottom">
				<button @click="navigate('login')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Login</button>
				<button @click="navigate('influencer-register')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Influencer Register</button>
				<button @click="navigate('sponsor-register')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Sponsor Register</button>
				<button @click="navigate('user-register')" class="sidebar-button btn btn-secondary btn-block mb-2">User
					Register</button>
				<hr class="bg-white">
				v 2.0.0
			</div>

		</div>

		<div class="main-content" id="main">
			<h4>{{ email }}</h4>
			<h4>{{ username }}</h4>
			<h4>{{ phno }}</h4>
			<h4>{{ industry }}</h4>

			<form @submit.prevent="updateSponsorDashboard">
				<input v-model="email" :placeholder="email" type="email" />
				<input v-model="password" type="password" placeholder="Password" required />
				<input v-model="username" :placeholder="username" type="text" required />
				<input v-model="phno" :placeholder="phno" type="text" required />
				<select v-model="industry" :placeholder="industry" type="text" required>
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
				<button type="submit">Login</button>
			</form>
			<div v-if="error">{{ error }}</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			email: '',
			username: '',
			phno: '',
			industry: ''
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/sponsor/update_dashboard', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.email = response.data.email;
			this.username = response.data.username;
			this.phno = response.data.ph_no;
			this.industry = response.data.industry;
		} catch (err) {
			this.$router.push('/login');
		}
	},
	methods: {
		async updateSponsorDashboard() {
			try {
				const response = await axios.post('http://localhost:5000/sponsor/update_dashboard', {
					pwd: this.password,
					username: this.username,
					phno: this.phno,
					industry: this.industry,
					next: this.$route.query.next
				}, {
					headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
				});
				console.log(response.data);
			} catch (err) {
				this.error = 'Invalid username or password';
			}
		},
		// Nav and Side Bar
		logout() {
			this.$router.push("/logout")
		},
		toggle() {
			const sidebar = document.getElementById("mySidebar");
			const main = document.getElementById("main");
			if (sidebar.style.width === "250px") {
				sidebar.style.width = "0";
				main.style.marginLeft = "0";
			} else {
				sidebar.style.width = "250px";
				main.style.marginLeft = "250px";
			}
		},
	}

};
</script>
<style scoped>
/* Nav and Side Bar */
.header-bar {
	display: flex;
	position: fixed;
	top: 0;
	width: 100%;
	height: 60px;
	background-color: #B97A57;
	padding: 10px 20px;
	align-items: center;
	z-index: 4;
}

.header-content {
	display: flex;
	align-items: center;
	width: 100%;
}

.logout-button {
	position: absolute;
	right: 20px;
	background-color: #38566E;
	color: white;
	border: 0px;

	border-radius: 30px;
	padding: 5px 20px;
	cursor: pointer;
	font-size: 16px;
}

.logout-button:hover {
	background-color: #32284E;
}


.openbtn {
	font-size: 20px;
	cursor: pointer;
	border-radius: 100%;
	background-color: #111;
	color: white;
	padding: 10px 15px;
	border: none;
}

.openbtn:hover {
	background-color: #444;
}

.logo-img {
	position: absolute;
	height: 60px;
	width: auto;
	left: 80px;
}

.sidebar {
	height: 100%;
	width: 0;
	position: fixed;
	z-index: 1;
	top: 60px;
	left: 0;
	color: white;
	overflow-x: hidden;
	transition: 0.5s;
	padding-top: 20px;
	justify-content: center;
	text-align: center;
	background: rgba(255, 255, 255, 0.5), url('@/assets/sidebar_bg.jpg');
	background-size: cover;
	background-position: center;
	backdrop-filter: blur(10px);
	scrollbar-width: none;
}

.sidebar::before {
	content: "";
	position: absolute;
	top: -20px;
	left: -20px;
	width: calc(100% + 40px);
	height: calc(100% + 0px);
	background: url('@/assets/sidebar_bg.jpg') no-repeat center center;
	background-size: cover;
	filter: blur(10px);
	z-index: -1;
}

.sidebar-button {
	position: relative;
	width: 100%;
	background-color: transparent;
	border-color: #38566E;
	color: white;
	padding: 5px 20px;
	cursor: pointer;
	font-size: 16px;
}

.sidebar-button:hover {
	background-color: #38566E;
}


.sidebar-buttons-top,
.sidebar-buttons-bottom {
	padding: 0 20px;
}

.sidebar-buttons-bottom {
	position: absolute;
	bottom: 100px;
	width: 100%;
}

.sidebar-bg {
	background-image: url('@/assets/sidebar_bg.jpg');
	filter: blur(8px);
}

@media screen and (max-height: 450px) {
	.sidebar {
		padding-top: 15px;
	}
}

.main-content {
	margin-top: 50px;
	transition: margin-left 0.5s;
	padding: 16px;
}
</style>