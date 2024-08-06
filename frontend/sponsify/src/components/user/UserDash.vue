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
				<button @click="$router.push('/UserDash')" class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/UserUpdateDashboard')" class="sidebar-button btn btn-secondary btn-block mb-2">Update Dashboard</button>
				<button @click="$router.push('/UserSearchInfluencer')" class="sidebar-button btn btn-secondary btn-block mb-2">Search Influencer</button>
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
			<div v-if="msg" class="success-message">
				{{ msg }}
				<button @click="closeMsg" class="msg-close-btn">
					&nbsp; &times; &nbsp;
				</button>
			</div>
			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">
						<h3>{{ info[1] }}</h3>
					</span>
				</div>
				<div class="card-body">
					Name : {{ info[1] }}
					<br>Email Id : {{ info[2] }}
					<br>Phone Number : {{ info[3] }}
					<br>Following : {{ followers[1].length }}					
				</div>
			</div>
			<div class="m-2 card">
				<div class="card-header">
					<span class="d-inline-block text-truncate" style="max-width: 1000px">
						Influencers Following</span>
				</div>
				<div class="card-body">
					<div v-if="influencers.length" class="admin-container">
						<div v-for="(data, index) in followers[1]" :key="index" class="card">
							<div class="card-header d-flex justify-content-between align-items-center">
								<h3 class=" text-truncate" style="max-width: 1000px">{{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][1] }}</h3>
								<div style="display: flex">
									<a  class="btn btn-danger" @click="unfollow(influencers.filter(influencer => followers[1].includes(influencer[0]))[index][0])">
										Unfollow </a>
								</div>
							</div>
							<div class="card-body">
								<p>Email ID: {{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][2] }}</p>
								<p>Phone Number: {{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][3] }}</p>
								<p>Category: {{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][5] }}</p>
								<p>Niche: {{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][6] }}</p>
								<p>Followers: {{ influencers.filter(influencer => followers[1].includes(influencer[0]))[index][7] }}</p>
							</div>
						</div>
					</div>
					<div v-else>
						<p>No Influencers Following.</p>
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
			info: '',
			followers: '',
			influencers: '',
			username: '',
			user_type: '',
			msg: "",
		};
	},
	async created() {
		try {
			this.msg = "";
			const response = await axios.get('http://localhost:5000/user/dashboard', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.info = response.data.info;
			this.followers = response.data.followers;
			this.influencers = response.data.influencers;
		} catch (err) {
			this.$router.push('/login');
		}
		const user_response = await axios.get('http://localhost:5000/get_username', {
			headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
		});
		this.username = user_response.data.username;
		this.user_type = user_response.data.user_type;
	},
	methods: {
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
		async unfollow(iid) {
			await axios.get('http://localhost:5000/user/unfollow/' + iid, {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.msg = "Influencer will be unfollowed shortly.";
		},
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

.main-content {
	margin-top: 50px;
	transition: margin-left 0.5s;
	padding: 16px;
}

.admin-container {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	/* 3 columns of equal width */
	grid-template-rows: auto;
	gap: 16px;
	width: 100%;
	padding: 16px;
	border-radius: 8px;
}

</style>