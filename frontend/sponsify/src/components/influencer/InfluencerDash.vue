<template>
    <div>
      <h1>Current User: {{ info }}</h1>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        info: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/dashboard', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.info = response.data.info;
      } catch (err) {
        this.$router.push('/login');
      }
    }
  
  };
  </script>
  