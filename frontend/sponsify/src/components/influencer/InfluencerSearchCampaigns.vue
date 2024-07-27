<template>
	<div>
		<div>
			<label for="startTime-select">Start time:</label>
			<select id="startTime-select" v-model="selectedTime">
				<option value="">All</option>
				<option v-for="time in unique_Time" :key="time" :value="time">{{ formatTimestamp(time) }}</option>
			</select>

			<label for="budget-select">Budget:</label>
			<select id="budget-select" v-model="selectedCategory">
				<option value="">All</option>
				<option v-for="budget in unique_budget" :key="budget" :value="budget">{{ budget }}</option>
			</select>
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
								<a href="#" class="btn btn-primary" @click="send_request(campaign.cid, campaign.sid, campaign.budget)">Send
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
		{{ campaigns }}
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
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/influencer/search_campaigns', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			
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
		}
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
</style>