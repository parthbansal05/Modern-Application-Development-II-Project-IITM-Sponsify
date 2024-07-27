<template>
	<div>
		<div>
			<label for="niche-select">Filter by Niche:</label>
			<select id="niche-select" v-model="selectedNiche">
				<option value="">All</option>
				<option v-for="niche in unique_niches" :key="niche" :value="niche">{{ niche }}</option>
			</select>

			<label for="category-select">Filter by Category:</label>
			<select id="category-select" v-model="selectedCategory">
				<option value="">All</option>
				<option v-for="category in unique_categories" :key="category" :value="category">{{ category }}</option>
			</select>

			<label for="sort-select">Sort by Followers:</label>
			<select id="sort-select" v-model="sortOrder">
				<option value="asc">Ascending</option>
				<option value="desc">Descending</option>
			</select>
		</div>

		<div class="m-2 card">
			<div class="card-header">
				<span class="d-inline-block text-truncate" style="max-width: 1000px">Influencers</span>
			</div>
			<div class="card-body">
				<div v-if="influencers.length" class="influencer-container">
					<div v-for="(influencer, index) in filteredInfluencers" :key="index" class="card">
						<div class="card-header">
							<h3>{{ influencer[1] }}</h3>
							<div style="display: flex; justify-content: space-between">
								<a href="#" class="btn btn-primary" @click="follow(influencer[0])">Follow</a>
							</div>
						</div>
						<div class="card-body">
							<p>Influencer ID: {{ influencer[0] }}</p>
							<p>Influencer Username: {{ influencer[1] }}</p>
							<p>Influencer Email: {{ influencer[2] }}</p>
							<p>Influencer phone number: {{ influencer[3] }}</p>
							<p>Influencer User type: {{ influencer[4] }}</p>
							<p>Influencer Category: {{ influencer[5] }}</p>
							<p>Influencer Niche: {{ influencer[6] }}</p>
							<p>Influencer Followers: {{ influencer[7] }}</p>
							<p>Influencer Industry: {{ influencer[8] }}</p>
							<p>Influencer Budget: {{ influencer[9] }}</p>
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
			influencers: [],
			unique_niches: [],
			unique_categories: [],
			selectedNiche: '',
			selectedCategory: '',
			sortOrder: 'asc',
			selectedCampaign: '',
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/user/search_influencer', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.influencers = response.data.influencers;
			this.unique_niches = response.data.unique_niches;
			this.unique_categories = response.data.unique_categories;
		} catch (err) {
			console.log(err);
		}
	},
	computed: {
		filteredInfluencers() {
			let filtered = this.influencers;

			if (this.selectedNiche) {
				filtered = filtered.filter(influencer => influencer[6] === this.selectedNiche);
			}

			if (this.selectedCategory) {
				filtered = filtered.filter(influencer => influencer[5] === this.selectedCategory);
			}

			if (this.sortOrder === 'asc') {
				filtered = filtered.sort((a, b) => a[7] - b[7]);
			} else {
				filtered = filtered.sort((a, b) => b[7] - a[7]);
			}

			return filtered;
		}
	},
	methods: {
		follow(influencer_id) {
			try {
				axios.get('http://localhost:5000/user/follow/' + influencer_id, {
					headers: {
						Authorization: `Bearer ${sessionStorage.getItem("token")}`,
					},
				});
			} catch (err) {
				console.error(err);
			}
			console.log(influencer_id);
		}
	}
};
</script>
<style scoped>
.influencer-container {
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