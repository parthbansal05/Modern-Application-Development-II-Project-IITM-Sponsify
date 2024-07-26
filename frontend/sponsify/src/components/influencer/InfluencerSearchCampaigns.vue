<template>
    <div>
      <h1>Current User: {{ campaigns }}</h1>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        campaigns: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/search_campaigns', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.campaigns = response.data.campaigns;
      } catch (err) {
        console.log(err);
      }
    }
  
  };
  </script>
  