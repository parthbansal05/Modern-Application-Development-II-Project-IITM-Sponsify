<template>
    <div>
      <h4>{{ influencers }}</h4>
      <h4>{{ campaigns }}</h4> 
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        influencers: [],
        campaigns: []
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/search_influencer', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.influencers = response.data.influencers;
        this.campaigns = response.data.campaigns;
      } catch (err) {
        console.log(err);
      }
    }
  
  };
  </script>
  