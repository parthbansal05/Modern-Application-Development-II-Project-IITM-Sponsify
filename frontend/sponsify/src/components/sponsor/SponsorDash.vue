<template>
	<div>
		<div class="m-2 card p-4">
			<h6>
				User Info:<br>
				ID: {{ info[0] }}<br>
				Name: {{ info[1] }}<br>
				Email: {{ info[2] }}<br>
				Phone Number: {{ info[3] }}<br>
				User Type: {{ info[4] }}<br>
				Category: {{ info[5] }}<br>
				Niche: {{ info[6] }}<br>
				Followers: {{ info[7] }}<br>
				Industry: {{ info[8] }}<br>
				Budget: {{ info[9] }}<br>
			</h6>
		</div>
		<div class="m-2 card">
			<div class="card-header">
				<span class="d-inline-block text-truncate" style="max-width: 1000px">Recent Campaigns</span>
			</div>
			<div class="card-body">
				<div v-if="campaigns.length" class="campaign-container">
					<div v-for="(campaign, index) in campaigns[0]" :key="index" class="card">
						<div class="card-header">
							<h3>{{ campaigns[2][index] }}</h3>
							<div style="display: flex; justify-content: space-between;">
								<a :href="`/SponsorViewCampaign/${campaigns[0][index]}`"
									class="btn btn-primary">View</a>
								<a v-if="campaigns[7][index] === 'Public'" href="#" class="btn btn-warning"
									@click="setVisibility(campaigns[0][index], 'Private')">Make Private</a>
								<a v-if="campaigns[7][index] === 'Private'" href="#" class="btn btn-success"
									@click="setVisibility(campaigns[0][index], 'Public')">Make Public</a>
								<a :href="`/UpdateCampaign/${campaigns[0][index]}`" class="btn btn-primary">Update</a>
								<a href="#" class="btn btn-primary"
									@click="delete_campaign(campaigns[0][index])">Delete</a>
							</div>
						</div>
						<div class="card-body">
							<p>Campaign ID: {{ campaigns[0][index] }}</p>
							<p>Sponsor ID: {{ campaigns[1][index] }}</p>
							<p>Title: {{ campaigns[2][index] }}</p>
							<p>Description: {{ campaigns[3][index] }}</p>
							<p>Start Time: {{ formatTimestamp(campaigns[4][index]) }}</p>
							<p>End Time: {{ formatTimestamp(campaigns[5][index]) }}</p>
							<p>Budget: {{ campaigns[6][index] }}</p>
							<p>Visibility: {{ campaigns[7][index] }}</p>
							<p>Goal: {{ campaigns[8][index] }}</p>
							<p>Flagged: {{ campaigns[9][index] }}</p>
							<br>
							<p>Campaign Progress</p>
							<div class="slider-container">
								<div class="slider" :id="'slider-' + index">
									<div class="slider-progress" :id="'slider-progress-' + index"></div>
								</div>
								<div class="timestamp-container">
									<span :id="'start-time-' + index">{{ formatTimestamp(campaigns[4][index]) }}</span>
									<span :id="'end-time-' + index">{{ formatTimestamp(campaigns[5][index]) }}</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<!-- <div v-else>
        <p>No campaigns available.</p>
      </div>  -->
	</div>
	<!-- </div> -->
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			campaigns: [],
			info: []
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/sponsor/dashboard', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.campaigns = response.data.campaigns;
			this.info = response.data.info;
			await new Promise((resolve) => setTimeout(resolve, 1000));
			for (let i = 0; i < this.campaigns[0].length; i++) {
				const startTime = this.campaigns[4][i] * 1000;
				const endTime = this.campaigns[5][i] * 1000;
				const currentTime = Date.now();
				const totalDuration = endTime - startTime;
				const elapsedDuration = currentTime - startTime;
				const percentage = Math.min((elapsedDuration / totalDuration) * 100, 100);

				const slider = document.getElementById('slider-progress-' + i);
				slider.style.width = percentage + '%';
			}
		} catch (err) {
			console.log(err);
		}
	},

	methods: {
		formatTimestamp(timestamp) {
			const date = new Date(timestamp * 1000);
			return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
		},
		async setVisibility(campaignID, visibility) {
			await axios.get('http://localhost:5000/sponsor/set_visibility/' + campaignID + '/' + visibility, {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			})
				.then((response) => {
					console.log(response);
					window.location.reload();
				})
				.catch((error) => {
					console.log(error);
				});
		},
		async delete_campaign(campaignID) {
			await axios.get('http://localhost:5000/sponsor/delete_campaign/' + campaignID, {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			})
				.then((response) => {
					console.log(response);
					window.location.reload();
				})
				.catch((error) => {
					console.log(error);
				});
		}


	}
};
</script>

<style scoped>
.info-card {
	border: 1px solid #ccc;
	overflow-wrap: break-word;
	padding: 16px;
	margin: 16px 0;
	border-radius: 8px;
	background-color: #f9f9f9;
}

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

.campaign-card {
	width: 30rem;
	overflow-wrap: break-word;
	border: 1px solid #ccc;
	padding: 16px;
	margin: 10px 0;
	background-color: #f9f9f9;
	box-sizing: border-box;
}

.campaign-card-header {
	position: relative;
	top: 0%;
	left: 0%;
	/* width: max-content; */
	overflow-wrap: break-word;
	border: 1px solid #ccc;
	padding: 16px;
	margin: 0px 0;
	background-color: #f9f9f9;
	box-sizing: border-box;
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
