<template>
  <div>
    <h6>
      {{ campaigns }} <br>
      {{ info }}<br>
    </h6>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      campaigns: '',
      info: ''
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
  }

};
</script>
