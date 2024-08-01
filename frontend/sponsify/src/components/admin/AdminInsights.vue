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
			<h3 class="sidebar-heading">{{username}}</h3>
			<h6 class="sidebar-subheading">{{ user_type }}</h6>

			<div class="sidebar-buttons-top">
				<hr class="bg-white">
				<button @click="$router.push('/AdminDash')" class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/AdminViewAllCampaigns')" class="sidebar-button btn btn-secondary btn-block mb-2">View All Campaigns</button>
				<button @click="$router.push('/AdminInsights')" class="sidebar-button btn btn-secondary btn-block mb-2">View Insights</button>
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
						<h6>Data Insights</h6></span>
				</div>

				<div class="card-body">
					<div class="admin-container">
						<div class="card">
							<div class="card-header d-flex justify-content-between align-items-center">
								Flagged Campaign Distribution
							</div>

							<div class="card-body">
								<canvas id="FlaggedCampaignChart"></canvas>
							</div>
						</div>

						<div class="card">
							<div class="card-header d-flex justify-content-between align-items-center">
								Campaign Visibility Distribution
							</div>

							<div class="card-body">
								<canvas id="PublicCampaignChart"></canvas>
							</div>
						</div>

						<div class="card">
							<div class="card-header d-flex justify-content-between align-items-center">
								User Status Distribution
							</div>

							<div class="card-body">								
								<canvas id="UserDistribututionCampaignChart"></canvas>
							</div>
						</div>

						<div class="card">
							<div class="card-header d-flex justify-content-between align-items-center">
								Campaign Approval Distribution
							</div>

							<div class="card-body">								
								<canvas id="StatusCampaignChart"></canvas>
							</div>
						</div>
					</div>	
					
					<div class="card custom-width">
						<div class="card-header d-flex justify-content-between align-items-center">
							Top Influencers
						</div>
						<div class="card-body">
							<canvas id="InfluencerFollowersChart"></canvas>
						</div>
					</div>
					
				</div>
			</div>

		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables, BarController, CategoryScale, PieController, ArcElement, Tooltip, Legend } from 'chart.js';

Chart.register(BarController, CategoryScale, PieController, ArcElement, Tooltip, Legend, ...registerables);

export default {
	data() {
		return {
			info: '',
			username: '',
			user_type: ''
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/admin/insights', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			});
			this.info = response.data.info;

			const user_response = await axios.get('http://localhost:5000/get_username', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			});
			this.username = user_response.data.username;
			this.user_type = user_response.data.user_type;

			this.renderChart();
		} catch (err) {
			console.error(err);
		}
	},
	methods: {
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
		renderChart() {
			if (this.info[0]) {
				const labels = this.info[0].map(item => item.label.replace(/_/g, ' '));
				const data = this.info[0].map(item => item.number);

				const ctx = document.getElementById('FlaggedCampaignChart').getContext('2d');
				new Chart(ctx, {
					type: 'pie',
					data: {
						labels: labels,
						datasets: [{
							data: data,
							backgroundColor: data.map(() => 'rgba(' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',0.5)')
						}]
					},
					options: {
						responsive: true,
						plugins: {
							legend: {
								position: 'top'
							},
							tooltip: {
								mode: 'index'
							}
						}
					}
				});
			}

			if (this.info[1]) {
				const labels = this.info[1].map(item => item.label.replace(/_/g, ' '));
				const data = this.info[1].map(item => item.number);

				const ctx = document.getElementById('PublicCampaignChart').getContext('2d');
				new Chart(ctx, {
					type: 'pie',
					data: {
						labels: labels,
						datasets: [{
							data: data,
							backgroundColor: data.map(() => 'rgba(' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',0.5)')
						}]
					},
					options: {
						responsive: true,
						plugins: {
							legend: {
								position: 'top'
							},
							tooltip: {
								mode: 'index'
							}
						}
					}
				});
			}

			if (this.info[2]) {
				const labels = this.info[2].map(item => item.label.replace(/_/g, ' '));
				const data = this.info[2].map(item => item.number);

				const ctx = document.getElementById('UserDistribututionCampaignChart').getContext('2d');
				new Chart(ctx, {
					type: 'pie',
					data: {
						labels: labels,
						datasets: [{
							data: data,
							backgroundColor: data.map(() => 'rgba(' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',0.5)')
						}]
					},
					options: {
						responsive: true,
						plugins: {
							legend: {
								position: 'top'
							},
							tooltip: {
								mode: 'index'
							}
						}
					}
				});
			}

			if (this.info[4]) {
				const labels = this.info[4].map(item => item.label.replace(/_/g, ' '));
				const data = this.info[4].map(item => item.number);

				const ctx = document.getElementById('StatusCampaignChart').getContext('2d');
				new Chart(ctx, {
					type: 'pie',
					data: {
						labels: labels,
						datasets: [{
							data: data,
							backgroundColor: data.map(() => 'rgba(' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',0.5)')
						}]
					},
					options: {
						responsive: true,
						plugins: {
							legend: {
								position: 'top'
							},
							tooltip: {
								mode: 'index'
							}
						}
					}
				});
			}

			if (this.info[3]) {
				const labels = this.info[3].map(item => item.label.replace(/_/g, ' '));
				const data = this.info[3].map(item => item.number);

				const ctx = document.getElementById('InfluencerFollowersChart').getContext('2d');
				new Chart(ctx, {
					type: 'bar',
					data: {
						labels: labels,
						datasets: [{
							data: data,
							backgroundColor: data.map(() => 'rgba(' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',' + Math.floor(Math.random() * 256) + ',0.5)')
						}]
					},
					options: {
						responsive: true,
						scales: {
							x: {
								beginAtZero: true,
								grid: {
									display: false
								}
							},
							y: {
								beginAtZero: true
							}
						},
						plugins: {
							legend: {
								display: false
							},
							tooltip: {
								mode: 'index'
							}
						}
					}
				});
			}

		}
	},
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

.admin-container {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	/* 3 columns of equal width */
	grid-template-rows: auto;
	gap: 16px;
	width: 100%;
	padding: 16px;
	border-radius: 8px;
}

.custom-width{
	margin-left: 15px;
	margin-right: 15px;
	width: 100% - 30px;
}

</style>