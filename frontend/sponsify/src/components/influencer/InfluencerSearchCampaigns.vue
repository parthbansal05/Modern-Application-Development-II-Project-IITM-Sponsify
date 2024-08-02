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
			<h3 class="sidebar-heading">{{ username }}</h3>
			<h6 class="sidebar-subheading">{{ user_type }}</h6>

			<div class="sidebar-buttons-top">
				<hr class="bg-white">
				<button @click="$router.push('/InfluencerDash')" class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/InfluencerUpdateDashboard')" class="sidebar-button btn btn-secondary btn-block mb-2">Update Dashboard</button>
				<button @click="$router.push('/InfluencerSearchCampaigns')" class="sidebar-button btn btn-secondary btn-block mb-2">Search Campaigns</button>
				<button @click="$router.push('/InfluencerInbox')" class="sidebar-button btn btn-secondary btn-block mb-2">Inbox</button>
			</div>

			<div class="sidebar-buttons-bottom">
				<button @click="$router.push('/login')" class="sidebar-button btn btn-secondary btn-block mb-2">Login</button>
				<button @click="$router.push('/registerInfluencer')" class="sidebar-button btn btn-secondary btn-block mb-2">Influencer Register</button>
				<button @click="$router.push('/registerSponsor')" class="sidebar-button btn btn-secondary btn-block mb-2">Sponsor Register</button>
				<button @click="$router.push('/registerUser')" class="sidebar-button btn btn-secondary btn-block mb-2">User Register</button>
				<hr class="bg-white">
				v 2.0.0
			</div>

		</div>

		<div class="main-content" id="main">

			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">
						Filter</span>
				</div>
				<div class="card-body filter-form">
					<div class="two-filters">
						<div>
							<label for="startTime-select"> Start Date and Time : &nbsp; </label>
							<select id="startTime-select" v-model="selectedTime">
								<option value="">All</option>
								<option v-for="time in unique_Time" :key="time" :value="time">{{ formatTimestamp(time) }}</option>
							</select>						
						</div>						
						<div>
							<label for="budget-select"> Budget : &nbsp; </label>
							<select id="budget-select" v-model="selectedCategory">
								<option value="">All</option>
								<option v-for="budget in unique_budget" :key="budget" :value="budget">{{ budget }}</option>
							</select>
						</div>
					</div>
				</div>
			</div>

			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">Campaigns</span>
				</div>
				<div class="card-body">
					<div v-if="campaigns.length" class="campaign-container">
						<div v-for="(campaign, index) in filteredCampaigns" :key="index" class="card">
							<div class="card-header">
								<h3>{{ campaign.title }}</h3>
								<div style="display: flex; justify-content: space-between">
									<a  class="btn btn-primary"
										@click="send_request(campaign.cid, campaign.sid, campaign.budget)">Send
										Request</a>
								</div>
							</div>
							<div class="card-body">
								<p>CID: {{ campaign.cid }}</p>
								<p>SID: {{ campaign.sid }}</p>
								<p>Name: {{ campaign.title }}</p>
								<p>Description: {{ campaign.description }}</p>
								<p>Start Date: {{ formatTimestamp(campaign.startDate) }}</p>
								<p>End Date: {{ formatTimestamp(campaign.endDate) }}</p>
								<p>Budget: {{ campaign.budget }}</p>
								<p>Visibility: {{ campaign.visibility }}</p>
								<p>Goals: {{ campaign.goal }}</p>
								<p>Flagged: {{ campaign.flagged }}</p>
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
			campaigns: [],
			unique_Time: [],
			unique_budget: [],
			selectedCategory: '',
			selectedTime: '',
			username: '',
			user_type: ''
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/influencer/search_campaigns', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			if (response.data.campaigns.length !== 0) {
			
				for (let i = 0; i < response.data.campaigns[0].length; i++) {
					const campaign = {
						cid: response.data.campaigns[0][i],
						sid: response.data.campaigns[1][i],
						title: response.data.campaigns[2][i],
						description: response.data.campaigns[3][i],
						startDate: response.data.campaigns[4][i],
						endDate: response.data.campaigns[5][i],
						budget: response.data.campaigns[6][i],
						visibility: response.data.campaigns[7][i],
						goal: response.data.campaigns[8][i],
						flagged: response.data.campaigns[9][i]
					};
					this.campaigns.push(campaign);
				}
				this.unique_Time = response.data.unique_start_times;
				this.unique_budget = response.data.unique_budgets;
			}

			const user_response = await axios.get('http://localhost:5000/get_username', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.username = user_response.data.username;
			this.user_type = user_response.data.user_type;
		} catch (err) {
			console.log(err);
		}
	},
	computed: {
		filteredCampaigns() {
			let filtered = this.campaigns;

			if (this.selectedTime) {
				filtered = filtered.filter(campaign => campaign.startDate === this.selectedTime);
			}

			if (this.selectedCategory) {
				filtered = filtered.filter(campaign => campaign.budget === this.selectedCategory);
			}
			console.log(filtered);
			return filtered;
		}
	},
	methods: {
		formatTimestamp(timestamp) {
			const date = new Date(timestamp * 1000);
			return date.toLocaleDateString() + " " + date.toLocaleTimeString();
		},
		send_request(cid, sid, budget) {
			try {
				axios.get('http://localhost:5000/influencer/initiate_chat/' + cid + '/' + sid + '/' + budget, {
					headers: {
						Authorization: `Bearer ${sessionStorage.getItem("token")}`,
					},
				});
			} catch (err) {
				console.error(err);
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
.campaign-container {
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

.two-filters{
	display: flex;
	justify-content: space-between;
	margin-left: 200px;
	margin-right: 200px;
	width: 100%-400px;
}

</style>