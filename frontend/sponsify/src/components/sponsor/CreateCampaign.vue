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
				<button @click="$router.push('/SponsorDash')" class="sidebar-button btn btn-secondary btn-block mb-2">Dashboard</button>
				<button @click="$router.push('/SponsorUpdateDashboard')" class="sidebar-button btn btn-secondary btn-block mb-2">Update Dashboard</button>
				<button @click="$router.push('/CreateCampaign')" class="sidebar-button btn btn-secondary btn-block mb-2">Create Campaign</button>
				<button @click="$router.push('/SponsorSearchInfluencer')" class="sidebar-button btn btn-secondary btn-block mb-2">Search Influencer</button>
				<button @click="$router.push('/SponsorInbox')" class="sidebar-button btn btn-secondary btn-block mb-2">Inbox</button>
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

		<div class="main-container" id="main">
			
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

			<form @submit.prevent="createCampaign" class="update-form">
				<input type="text" v-model="campTitle" placeholder="Campaign Title" required>
				<input type="text" v-model="campDesc" placeholder="Campaign Description" required>
				<input type="date" v-model="startDate" placeholder="Start Date" required>
				<input type="date" v-model="endDate" placeholder="End Date" required>
				<input type="number" v-model="budget" placeholder="Budget" required>
				<select v-model="visibility" required>
					<option value="Public">Public</option>
					<option value="Private">Private</option>
				</select>
				<input type="text" v-model="goal" placeholder="Goal" required>
				<button type="submit">Create</button>
			</form>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			campTitle: '',
			campDesc: '',
			startDate: '',
			endDate: '',
			budget: '',
			visibility: 'Public',
			goal: '',
			error: '',
			username: '',
			user_type: '',
			msg: ''
		};
	},
	async created() {
		try {
			const user_response = await axios.get('http://localhost:5000/get_username', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.username = user_response.data.username;
			this.user_type = user_response.data.user_type;
		} catch (err) {
			this.$router.push('/login');
		}
	},
	methods: {
		async createCampaign() {
			try {
				this.error = '';
				this.msg = '';
				const response = await axios.post('http://localhost:5000/sponsor/create_campaign', {
					campTitle: this.campTitle,
					campDesc: this.campDesc,
					startDate: this.startDate,
					endDate: this.endDate,
					budget: this.budget,
					visibility: this.visibility,
					goal: this.goal,
					next: this.$route.query.next
				}, {
					headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
				});

				
				if ('error' in response.data) {
					this.error = response.data.error;
					return;
				}
				if ('msg' in response.data) {
					this.msg = response.data.msg;
					return;
				}

				console.log(response.data);
			} catch (err) {
				this.error = 'Invalid username or password';
			}
		},
		closeError() {
			this.error = null
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

.main-container {
	display: flex;
	flex-direction: column;
	position: fixed;
	width: 100%;
	height: 100vh;
	padding-top: 30px;
	transition: margin-left 0.5s;
	align-items: center;
	justify-content: center;
	background-image: url('@/assets/background.jpeg');
	background-size: cover;
	background-position: center;
}

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

.update-form {
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

.update-form input {
	margin-bottom: 1rem;
	padding: 0.5rem;
	font-size: 1rem;
	background-color: #FFFFFF;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.update-form button {	
	padding: 0.5rem;
	font-size: 1rem;
	color: white;
	background-color: #38566E;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

.update-form select {
	margin-bottom: 1rem;
	padding: 0.5rem;
	font-size: 1rem;
	background-color: #FFFFFF;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.update-form button:hover {
	background-color: #B97A57;
}
</style>