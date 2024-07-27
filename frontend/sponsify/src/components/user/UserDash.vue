<template>
  <div>
    <div class="m-2 card p-4">
      <h6>
        User Info:<br>
        Current User: {{ info }}
        Followers: {{ followers }}
        Influencers: {{ influencers }}
      </h6>
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
      influencers: ''
    };
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:5000/user/dashboard', {
        headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
      });
      this.info = response.data.info;
      this.followers = response.data.followers;
      this.influencers = response.data.influencers;
    } catch (err) {
      this.$router.push('/login');
    }
  }

};
</script>