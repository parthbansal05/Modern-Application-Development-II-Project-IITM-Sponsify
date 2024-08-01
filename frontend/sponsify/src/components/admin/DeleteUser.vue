<template>
	<div>
		<h1>User Deletion {{ status }}, for User ID {{ id }}</h1>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			id: this.$route.params.id,
			status: 'Pending'
		};
	},
	async created() {
		try {
			const response = await axios.get('http://localhost:5000/delete_user/' + this.id, {
				headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
			});
			this.status = response.data.status;
		} catch (err) {
			console.log(err);
		}
	}

};
</script>