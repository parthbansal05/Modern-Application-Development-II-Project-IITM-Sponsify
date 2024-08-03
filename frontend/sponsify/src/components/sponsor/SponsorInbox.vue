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

			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">
						Inbox
					</span>
				</div>

				<div class="card-body">
					<div v-if="inbox[0].length">
						<div v-for="(aid, index) in inbox[0]" :key="index" class="m-2 card ">
							
							<div class="card-header d-flex justify-content-between">
								<div class="d-flex align-items-center justify-content-center">	
									<h5 class=" text-truncate" style="max-width: 1000px">
										{{ influencer.filter(infl => infl[0] === inbox[3][index])[0][1] }}
									</h5>
								</div>

								<a  class="btn btn-primary" @click="delete_chat(inbox[3][index], userID)">
									Delete
								</a>
							</div>

							<a :href="`/SponsorInboxChat/${inbox[3][index]}`" style="color: black; text-decoration: none;">
								<div class="card-body">
									<h4 class=" text-truncate" style="max-width: 1000px">{{ inbox[7][index] }}</h4> 
									Budget : {{ inbox[8][index] }}
									<br>
									<div v-if="inbox[9][index].length">
										<span class="d-inline-block text-truncate" style="max-width: 1000px">Terms : {{ inbox[9][index] }} </span>
									</div>
									<div v-if="inbox[10][index] == 'False'" class="dot"></div>
								</div>
							</a>
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
import axios from 'axios';

export default {
	data() {
		return {
			inbox: '',
			camp_dict: '',
			influencer: '',
			username: '',
			user_type: '',
			userID: '',
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/sponsor/inbox', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.inbox = response.data.inbox;
			this.camp_dict = response.data.camp_dict;
			this.influencer = response.data.influencer;
			this.userID = response.data.userID;
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
		async delete_chat(iid, sid) {
			console.log('http://localhost:5000/delete_chat/' + iid + '/' + sid + '/True');
			await axios.get('http://localhost:5000/delete_chat/' + iid + '/' + sid + '/True', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			window.location.reload();
		},
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

.dot{
	position: absolute;
	height: 15px;
	width: 15px;
	background-color: green;
	border-radius: 50%;
	/* display: inline-block; */
	right: 25px;
	bottom: 20px;
}
</style>