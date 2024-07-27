<template>
	<div>
		<div class="m-2 card p-4">
			<h6>
				{{ campaigns }} <br>
				{{ users }}<br>
				{{ influencer }}<br>
				{{ sponsors }}<br>
				{{ camp_dict }}<br>
				{{ admin_email }}<br>
				{{ admin_phno }}<br>
			</h6>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			campaigns: '',
			users: '',
			influencer: '',
			sponsors: '',
			camp_dict: '',
			admin_email: '',
			admin_phno: ''
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/admin/dashboard', {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
			});
			this.campaigns = response.data.campaigns;
			this.users = response.data.users;
			this.influencer = response.data.influencer;
			this.sponsors = response.data.sponsors;
			this.camp_dict = response.data.camp_dict;
			this.admin_email = response.data.admin_email;
			this.admin_phno = response.data.admin_phno;
		} catch (err) {
			console.log(err);
		}
	}

};
</script>