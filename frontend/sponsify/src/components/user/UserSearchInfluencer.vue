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
			<h3 class="sidebar-heading"><span class="d-inline-block text-truncate" style="max-width: 150px">{{ username
					}}</span></h3>
			<h6 class="sidebar-subheading">{{ user_type }}</h6>

			<div class="sidebar-buttons-top">
				<hr class="bg-white">
				<button @click="$router.push('/UserDash')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/UserUpdateDashboard')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Update Dashboard</button>
				<button @click="$router.push('/UserSearchInfluencer')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Search Influencer</button>
			</div>

			<div class="sidebar-buttons-bottom">
				<button @click="$router.push('/login')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Login</button>
				<button @click="$router.push('/registerInfluencer')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Influencer Register</button>
				<button @click="$router.push('/registerSponsor')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Sponsor Register</button>
				<button @click="$router.push('/registerUser')"
					class="sidebar-button btn btn-secondary btn-block mb-2">User Register</button>
				<hr class="bg-white">
				v 2.0.0
			</div>

		</div>

		<div class="main-content" id="main">
			<div v-if="msg" class="success-message">
				{{ msg }}
				<button @click="closeMsg" class="msg-close-btn">
					&nbsp; &times; &nbsp;
				</button>
			</div>
			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">Filter</span>
				</div>
				<div class="card-body filter-form">
					<div class="three_filters">
						<div>
							<label for="niche-select">Filter by Niche : &nbsp; </label>
							<select id="niche-select" v-model="selectedNiche">
								<option value="">All</option>
								<option v-for="niche in unique_niches" :key="niche" :value="niche">{{ niche }}</option>
							</select>
						</div>
						<div>
							<label for="category-select">Filter by Category : &nbsp; </label>
							<select id="category-select" v-model="selectedCategory">
								<option value="">All</option>
								<option v-for="category in unique_categories" :key="category" :value="category">{{
									category
									}}
								</option>
							</select>
						</div>
						<div>
							<label for="sort-select">Sort by Followers : &nbsp; </label>
							<select id="sort-select" v-model="sortOrder">
								<option value="asc">Ascending</option>
								<option value="desc">Descending</option>
							</select>
						</div>
					</div>
				</div>
			</div>

			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">Influencers</span>
				</div>
				<div class="card-body">
					<div v-if="influencers.length" class="influencer-container">
						<div v-for="(influencer, index) in filteredInfluencers" :key="index" class="card">
							<div class="card-header">
								<h3 class=" text-truncate" style="max-width: 1000px">{{ influencer[1] }}</h3>
								<div style="display: flex; justify-content: space-between">
									<a class="btn btn-primary" @click="follow(influencer[0])">Follow</a>
								</div>
							</div>
							<div class="card-body">
								<!-- <p>Influencer ID: {{ influencer[0] }}</p> -->
								<p class=" text-truncate" style="max-width: 1000px">Influencer Username: {{
									influencer[1] }}</p>
								<p>Influencer Email: {{ influencer[2] }}</p>
								<p>Influencer phone number: {{ influencer[3] }}</p>
								<!-- <p>Influencer User type: {{ influencer[4] }}</p> -->
								<p>Influencer Category: {{ influencer[5] }}</p>
								<p>Influencer Niche: {{ influencer[6] }}</p>
								<p>Influencer Followers: {{ influencer[7] }}</p>
								<!-- <p>Influencer Industry: {{ influencer[8] }}</p>
								<p>Influencer Budget: {{ influencer[9] }}</p> -->
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			influencers: [],
			unique_niches: [],
			unique_categories: [],
			selectedNiche: '',
			selectedCategory: '',
			sortOrder: 'desc',
			selectedCampaign: '',
			username: '',
			user_type: '',
			msg: '',
		};
	},
	async created() {
		try {
			this.msg = "";
			const response = await axios.get('http://localhost:5000/user/search_influencer', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.influencers = response.data.influencers;
			this.unique_niches = response.data.unique_niches;
			this.unique_categories = response.data.unique_categories;
		} catch (err) {
			console.log(err);
		}
		const user_response = await axios.get('http://localhost:5000/get_username', {
			headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
		});
		this.username = user_response.data.username;
		this.user_type = user_response.data.user_type;
	},
	computed: {
		filteredInfluencers() {
			let filtered = this.influencers;

			if (this.selectedNiche) {
				filtered = filtered.filter(influencer => influencer[6] === this.selectedNiche);
			}

			if (this.selectedCategory) {
				filtered = filtered.filter(influencer => influencer[5] === this.selectedCategory);
			}

			if (this.sortOrder === 'asc') {
				filtered = filtered.sort((a, b) => a[7] - b[7]);
			} else {
				filtered = filtered.sort((a, b) => b[7] - a[7]);
			}

			return filtered;
		}
	},
	methods: {
		async follow(influencer_id) {
			try {
				await axios.get('http://localhost:5000/user/follow/' + influencer_id, {
					headers: {
						Authorization: `Bearer ${sessionStorage.getItem("token")}`,
					},
				});
			} catch (err) {
				console.error(err);
			}
			this.msg = "Influencer followed successfully!";
		},
		closeMsg() {
			this.msg = null
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
.influencer-container {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	/* 3 columns of equal width */
	grid-template-rows: auto;
	gap: 16px;
	width: 100%;
	/* border: 1px solid #ccc; */
	padding: 16px;
	/* margin: 16px 0; */
	border-radius: 8px;
	/* background-color: #f9f9f9; */
	/* gap: 16px; */
}

.success-message {
	display: flex;
	/* width: 50rem; */
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

.filter-form select {
	width: 300px;
	margin-bottom: 1rem;
	padding: 0.5rem;
	font-size: 1rem;
	background-color: #FFFFFF;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.three_filters {
	display: flex;
	justify-content: space-between;
	margin-left: 50px;
	margin-right: 50px;
	width: 100%-400px;
}
</style>