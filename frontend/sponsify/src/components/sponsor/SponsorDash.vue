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
			<h3 class="sidebar-heading"><span class="d-inline-block text-truncate" style="max-width: 150px">{{ username }}</span></h3>
			<h6 class="sidebar-subheading">{{ user_type }}</h6>

			<div class="sidebar-buttons-top">
				<hr class="bg-white">
				<button @click="$router.push('/SponsorDash')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/SponsorUpdateDashboard')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Update Dashboard</button>
				<button @click="$router.push('/CreateCampaign')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Create Campaign</button>
				<button @click="$router.push('/SponsorSearchInfluencer')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Search Influencer</button>
				<button @click="$router.push('/SponsorInbox')"
					class="sidebar-button btn btn-secondary btn-block mb-2">Inbox</button>
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

			<!-- Main Content -->
			<div class="m-2 card p-4">
				<h6>
					User Info:<br />
					<!-- ID: {{ info[0] }}<br /> -->
					Name: {{ info[1] }}<br />
					Email: {{ info[2] }}<br />
					Phone Number: {{ info[3] }}<br />
					<!-- User Type: {{ info[4] }}<br /> -->
					<!-- Category: {{ info[5] }}<br />
					Niche: {{ info[6] }}<br /> -->
					<!-- Followers: {{ info[7] }}<br /> -->
					Industry: {{ info[8] }}<br />
					<!-- Budget: {{ info[9] }}<br /> -->
				</h6>
			</div>
			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">Recent Campaigns</span>
					<div style="text-align: right; padding-right: 10px;">
						<a  class="btn btn-primary" @click="GenReport(info[0])">Download Campaign Report</a>
					</div>
				</div>
				<div class="card-body">
					<div v-if="campaigns.length" class="campaign-container">
						<div v-for="(campaign, index) in campaigns[0]" :key="index" class="card">
							<div class="card-header">
								<h3 class=" text-truncate" style="max-width: 1000px">{{ campaigns[2][index] }}</h3>
								<div style="display: flex; justify-content: space-between">
									<a :href="`/SponsorViewCampaign/${campaigns[0][index]}`"
										class="btn btn-primary">View</a>
									<a v-if="campaigns[7][index] === 'Public'"  class="btn btn-warning"
										@click="setVisibility(campaigns[0][index], 'Private')">Make Private</a>
									<a v-if="campaigns[7][index] === 'Private'"  class="btn btn-success"
										@click="setVisibility(campaigns[0][index], 'Public')">Make Public</a>
									<a :href="`/UpdateCampaign/${campaigns[0][index]}`"
										class="btn btn-primary">Update</a>
									<a  class="btn btn-primary"
										@click="delete_campaign(campaigns[0][index])">Delete</a>
								</div>
							</div>
							<div class="card-body">
								<!-- <p>Campaign ID: {{ campaigns[0][index] }}</p>
								<p>Sponsor ID: {{ campaigns[1][index] }}</p> -->
								<p class=" text-truncate" style="max-width: 1000px">Title: {{ campaigns[2][index] }}</p>
								<p class=" text-truncate" style="max-width: 1000px">Description: {{ campaigns[3][index] }}</p>
								<p>Start Time: {{ formatTimestamp(campaigns[4][index]) }}</p>
								<p>End Time: {{ formatTimestamp(campaigns[5][index]) }}</p>
								<p>Budget: {{ campaigns[6][index] }}</p>
								<p>Visibility: {{ campaigns[7][index] }}</p>
								<p class=" text-truncate" style="max-width: 1000px">Goal: {{ campaigns[8][index] }}</p>
								<p>Flagged: {{ campaigns[9][index] }}</p>
								<br />
								<p>Campaign Progress</p>
								<div class="slider-container">
									<div class="slider" :id="'slider-' + index">
										<div class="slider-progress" :id="'slider-progress-' + index"></div>
									</div>
									<div class="timestamp-container">
										<span :id="'start-time-' + index">{{ formatTimestamp(campaigns[4][index])
											}}</span>
										<span :id="'end-time-' + index">{{ formatTimestamp(campaigns[5][index])
											}}</span>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div v-else>
						<p>No campaigns available.</p>
					</div>
				</div>
			</div>

		</div>
	</div>
</template>

<script>
import axios from "axios";

export default {
	data() {
		return {
			campaigns: [],
			info: [],
			username: "",
			user_type: "",
			msg: '',
		};
	},
	async created() {
		try {
			this.msg = "";
			const response = await axios.get(
				"http://localhost:5000/sponsor/dashboard",
				{
					headers: {
						Authorization: `Bearer ${sessionStorage.getItem("token")}`,
					}, // Change to sessionStorage
				}
			);
			this.campaigns = response.data.campaigns;
			this.info = response.data.info;
			await new Promise((resolve) => setTimeout(resolve, 1000));
			if (this.campaigns.length !== 0) {
				for (let i = 0; i < this.campaigns[0].length; i++) {
					const startTime = this.campaigns[4][i] * 1000;
					const endTime = this.campaigns[5][i] * 1000;
					const currentTime = Date.now();
					const totalDuration = endTime - startTime;
					const elapsedDuration = currentTime - startTime;
					const percentage = Math.min(
						(elapsedDuration / totalDuration) * 100,
						100
					);

					const slider = document.getElementById("slider-progress-" + i);
					slider.style.width = percentage + "%";
				}
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

	methods: {
		formatTimestamp(timestamp) {
			const date = new Date(timestamp * 1000);
			return date.toLocaleDateString() + " " + date.toLocaleTimeString();
		},
		logout() {
			this.$router.push("/logout")
		},
		async setVisibility(campaignID, visibility) {
			await axios
				.get(
					"http://localhost:5000/sponsor/set_visibility/" +
					campaignID +
					"/" +
					visibility,
					{
						headers: {
							Authorization: `Bearer ${sessionStorage.getItem("token")}`,
						},
					}
				)
				.then(() => {
					this.msg = 'Visibility will be updated shortly.';
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async GenReport(UserID) {
			sessionStorage.removeItem('ReportID');
			const response = await axios.get("http://localhost:5000/tasks/sponsor_export/" + UserID, { headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}`, }, });
			sessionStorage.setItem('ReportID', response.data.result_id);
			this.msg = 'Report will be generated shortly.';

		},
		async delete_campaign(campaignID) {
			await axios
				.get("http://localhost:5000/sponsor/delete_campaign/" + campaignID, {
					headers: {
						Authorization: `Bearer ${sessionStorage.getItem("token")}`,
					},
				})
				.then((response) => {
					console.log(response);
					this.msg = 'Campaign will be deleted shortly.';
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async fetch_CSV() {
			var ReportID = sessionStorage.getItem('ReportID');
			if (ReportID === null) {
				return;
			}
			const response = await axios.get("http://localhost:5000/tasks/result/" + ReportID, { headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}`, }, });

			if (response.data.ready === true && response.data.successful === true){
				sessionStorage.removeItem('ReportID');
				const blob = new Blob([response.data.value], { type: 'text/csv' });
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.href = url;
				a.download = 'report.csv';
				a.click();
				window.URL.revokeObjectURL(url);
			}
			else {
				console.log("CSV Not Ready");
			}
		},
		closeMsg() {
			this.msg = null
		},
		// Nav and Side Bar
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
	},
	mounted() {
		// Start the interval to run the function periodically
		setInterval(this.fetch_CSV, 2000); // Run every 5 seconds
	},
};
</script>

<style scoped>

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


/* Main Content */

.main-content {
	margin-top: 50px;
	transition: margin-left 0.5s;
	padding: 16px;
}

.campaign-container {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	/* 3 columns of equal width */
	grid-template-rows: auto;
	gap: 16px;
	width: 100%;
	padding: 16px;
	border-radius: 8px;
}

.slider-container {
	width: 100%;
}

.slider {
	width: 100%;
	height: 10px;
	background-color: #ddd;
	position: relative;
	border-radius: 5px;
}

.slider-progress {
	height: 100%;
	background-color: #4caf50;
	width: 0;
	border-radius: 5px;
}

.timestamp-container {
	display: flex;
	justify-content: space-between;
	margin-top: 10px;
}

.timestamp-container span {
	font-size: 14px;
}
</style>