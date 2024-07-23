<template>
    <div>
      <h4>{{ campaigns }}</h4>
      <h4>{{ sponsors }}</h4>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        campaigns: "",
        sponsors: "",
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/admin/view_all_campaigns', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.campaigns = response.data.campaigns;
        this.sponsors = response.data.sponsors;
      } catch (err) {
        console.error(err);
      }
    }
  
  };
  </script>
  