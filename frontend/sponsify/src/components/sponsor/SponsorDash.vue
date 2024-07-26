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
				Category: {{ info[8] }}<br>
				Niche: {{ info[5] }}<br>
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

					<div v-for="(campaign, index) in campaigns" :key="index" class="card">

						<div class="card-header">
							<h3>Campaign {{ index + 1 }}</h3>
							<div style="display: flex; justify-content: space-between;">
							<a href="#" class="btn btn-primary">View</a>
							<a href="#" class="btn btn-warning">Make Private</a>
							<a href="#" class="btn btn-success">Make Public</a>
							<a href="#" class="btn btn-primary">Update</a>
							<a href="#" class="btn btn-primary">Delete</a>
						</div>
						</div>

						<div class="card-body">

							<p>Campaign Number: {{ campaign[0] }}</p>
							<p>Sponsor ID: {{ campaign[1] }}</p>
							<p>Title: {{ campaign[2] }}</p>
							<p>Description: {{ campaign[3] }}</p>
							<p>Start Time: {{ formatTimestamp(campaign[4]) }}</p>
							<p>End Time: {{ formatTimestamp(campaign[5]) }}</p>
							<p>Budget: {{ campaign[6] }}</p>
							<p>Accessibility: {{ campaign[7] }}</p>
							<p>Goal: {{ campaign[8] }}</p>
							<p>Flagged: {{ campaign[9] }}</p>
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
		} catch (err) {
			console.log(err);
		}
	},
	methods: {
		formatTimestamp(timestamp) {
			const date = new Date(timestamp * 1000);
			return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
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
</style>
