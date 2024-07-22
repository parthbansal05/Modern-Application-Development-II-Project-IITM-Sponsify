<template>
    <div>
      <h1>Current User: {{ username }}</h1>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.username = response.data.username;
      } catch (err) {
        this.$router.push('/login');
      }
    }
  
  };
  </script>
  