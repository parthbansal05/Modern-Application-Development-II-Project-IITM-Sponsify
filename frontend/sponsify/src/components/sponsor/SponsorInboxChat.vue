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

			<div v-if="error">{{ error }}</div>

			<div class="col-lg-8 col-md-8 m-auto card" style="padding-bottom: 50px; width: 80%;">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">
						<h6> {{ influencer[1] }} </h6>
					</span>
				</div>

				<div v-if="showDialog" class="modal-overlay">
					<div class="modal-content">
						<h3>Campaign Details</h3>
							<p>Campaign Name:{{campaignName}}</p>
							<p>Campaign Description:{{campaignDesc}}</p>
							<p>Campaign Start Date:{{campaignSDate}}</p>
							<p>Campaign End Date:{{campaignEDate}}</p>
							<p>Campaign Budget:{{campaignBudget}}</p>
							<p>Campaign Visibility:{{campaignVisibility}}</p>
							<p>Campaign Goals:{{campaignGoal}}</p>
						<button @click="closeDialog">Close</button>
					</div>
				</div>

				<div v-for="(aid, index) in inbox[0]" :key="index" class="card-body">
					<div v-if="inbox[4][index] == 'INFL'" class="col-lg-10 col-md-6 ms-0 me-auto card p-3"
						style="background-color: #C4A484;">
						<h5> {{ inbox[7][index] }} </h5>
						<span>Budget Negotiation: {{ inbox[8][index] }}</span>
						<div v-if="inbox[9][index] != ''">
							Terms Negotiation : {{ inbox[9][index] }}
						</div>
						<h6 class="d-inline-block text-truncate" style="max-width: 200px; font-weight: normal;"
							@click="open_campaign_details(inbox[1][index])">
							Campaign : {{ camp_dict[inbox[1][index]] }} 
						</h6>

						<div class="bottom-right">
							<!-- Status -->
							<div>
								<div v-if="inbox[5][index] == 'Rejected'" class="dot_r" title="Rejected"></div>
								<div v-if="inbox[5][index] == 'PENDING'" class="dot_y" title="Pending"></div>
								<div v-if="inbox[5][index] == 'Approved'" class="dot_g" title="Approved"></div>
							</div>

							<!-- TimeStamp -->
							{{ formatTimestamp(inbox[6][index]) }}
						</div>

					</div>

					<div v-else-if="inbox[4][index] == 'SOPN'" class="col-lg-10 col-md-6 ms-auto me-0 card p-3"
						style="background-color: #FF5CCE;">

						<h5> {{ inbox[7][index] }} </h5>
						<span>Budget Negotiation: {{ inbox[8][index] }}</span>
						<div v-if="inbox[9][index] != ''">
							Terms Negotiation : {{ inbox[9][index] }}
						</div>
						<h6 class="d-inline-block text-truncate" style="max-width: 200px; font-weight: normal;"
							@click="open_campaign_details(inbox[1][index])">
							Campaign : {{ camp_dict[inbox[1][index]] }}
						</h6>

						<div class="bottom-right" style="position: absolute; right: 40px;">
							<!-- Status -->
							<div>
								<div v-if="inbox[5][index] == 'Rejected'" class="dot_r" title="Rejected"></div>
								<div v-if="inbox[5][index] == 'PENDING'" class="dot_y" title="Pending"></div>
								<div v-if="inbox[5][index] == 'Approved'" class="dot_g" title="Approved"></div>
							</div>

							<!-- TimeStamp -->
							{{ formatTimestamp(inbox[6][index]) }}
						</div>

						<!-- Tick and Double Tick -->
						<div v-if="inbox[11][index] == 'False'" style="position: absolute; bottom: 8px; right: 10px;">
							&#10004;
						</div>
						<div v-if="inbox[11][index] == 'True'">
							<div style="position: absolute; bottom: 8px; right: 14px;">
								&#10004;
							</div>
							<div style="position: absolute; bottom: 8px; right: 7px;">
								&#10004;
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="fixed-bottom-bar">
				<div class="container py-3 d-flex justify-content-between align-items-center">
					<form @submit.prevent="sendMsg" class="w-100">
						<div class="row align-items-center">
							<div class="col-md-4 mb-2 mb-md-0">
								<input type="text" v-model="msg" class="form-control" placeholder="Write a message">
							</div>
							<div class="col-md-8 d-flex flex-column flex-md-row align-items-center gap-3">
								<select v-model="campain_id" class="form-select mb-2 mb-md-0"
									placeholder="Select Campaign" required>
									<option
										v-for="(cid, index) in inbox[1].filter((cid, index) => inbox[1].indexOf(cid) === index)"
										:key="index" :value="cid">
										{{ camp_dict[cid] }}
									</option>
								</select>
								<input type="number" v-model="modified_budget" class="form-control mb-2 mb-md-0"
									placeholder="Modified Budget">
								<input type="text" v-model="modified_terms" class="form-control mb-2 mb-md-0"
									placeholder="Modified terms">
								<div class="d-flex gap-2 mb-2 mb-md-0">
									<a class="btn btn-success" @click="acceptOffer()">Accept</a>
									<a class="btn btn-danger" @click="rejectOffer()">Reject</a>
									<button type="submit" class="btn btn-primary">Send</button>
								</div>
							</div>
						</div>
					</form>
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
			inbox: '',
			camp_dict: '',
			influencer: '',
			msg: '',
			campain_id: "",
			modified_budget: '',
			modified_terms: '',
			username: '',
			user_type: '',
			campaignDetails: "",
			campaignName: "",
			campaignDesc: "",
			campaignSDate: "",
			campaignEDate: "",
			campaignBudget: "",
			campaignVisibility: "",
			campaignGoal: "",
			showDialog: false,
			userid: "",
			id: this.$route.params.id
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/sponsor/inbox/' + this.id, {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.inbox = response.data.inbox;
			this.camp_dict = response.data.camp_dict;
			this.influencer = response.data.influencer;
			this.userid = response.data.userID;
			this.campain_id = this.inbox[1].filter((cid, index) => this.inbox[1].indexOf(cid) === index)[0]
		} catch (err) {
			console.log(err);
		}
		const user_response = await axios.get('http://localhost:5000/get_username', {
			headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
		});
		this.username = user_response.data.username;
		this.user_type = user_response.data.user_type;
	},
	methods: {
		async sendMsg() {
			try {
				await axios.post('http://localhost:5000/sponsor/inbox/' + this.id, {
					message: this.msg,
					campaign: this.campain_id,
					modified_budget: this.modified_budget,
					modified_terms: this.modified_terms,
					next: this.$route.query.next
				}, {
					headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
				});
				window.location.reload();
			} catch (err) {
				this.error = 'Invalid username or password';
			}
		},
		async open_campaign_details(campaignId) {
			try {
				const response = await axios.get(`http://localhost:5000/view_campaign/${campaignId}`, {
					headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
				});
				this.campaignName = response.data.campaign[2][0];
				this.campaignDesc = response.data.campaign[3][0];
				this.campaignSDate = response.data.campaign[4][0];
				this.campaignEDate = response.data.campaign[5][0];
				this.campaignBudget = response.data.campaign[6][0];
				this.campaignVisibility = response.data.campaign[7][0];
				this.campaignGoal = response.data.campaign[8][0];
				this.showDialog = true;
			} catch (error) {
				console.error('Error fetching campaign details:', error);
			}
		},
		closeDialog() {
			this.showDialog = false;
		},
		async acceptOffer() {
			await axios.get('http://localhost:5000/sponsor/accept_ad_request/' + this.influencer[0] + '/' + this.userid + '/' + this.campain_id + '/Approved', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			});
			window.location.reload();
		},
		async rejectOffer() {
			await axios.get('http://localhost:5000/sponsor/accept_ad_request/' + this.influencer[0] + '/' + this.userid + '/' + this.campain_id + '/Rejected', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			});
			window.location.reload();
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
		formatTimestamp(timestamp) {
			const date = new Date(timestamp * 1000);
			return date.toLocaleDateString() + " " + date.toLocaleTimeString();
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
	margin-bottom: 40px;
	transition: margin-left 0.5s;
	padding: 16px;
}

.bottom-right {
	display: flex;
	justify-content: right;
	position: absolute;
	bottom: 5px;
	right: 10px;
	display: flex;
	gap: 6px;
	width: 100%;
}

.dot_g {
	height: 10px;
	width: 10px;
	background-color: #00DD00;
	border-radius: 50%;
	display: inline-block;
}

.dot_y {
	height: 10px;
	width: 10px;
	background-color: yellow;
	border-radius: 50%;
	display: inline-block;
}

.dot_r {
	height: 10px;
	width: 10px;
	background-color: red;
	border-radius: 50%;
	display: inline-block;
}

.fixed-bottom-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	width: 100%;
	background-color: #f8f9fa;
	padding: 10px;
	z-index: 0;
	transition: margin-left 0.5s;
	/* Ensure it appears above other content */
}
</style>