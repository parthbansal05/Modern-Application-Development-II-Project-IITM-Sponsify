<template>
    <div>
      <h1>Current User: {{ influencers }}</h1>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        influencers: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/user/search_influencer', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.influencers = response.data.influencers;
      } catch (err) {
        console.log(err);
      }
    }
  
  };
  </script>
  