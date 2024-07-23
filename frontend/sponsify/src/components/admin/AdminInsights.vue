<template>
    <div>
      <h4>{{ info }}</h4>
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
        const response = await axios.get('http://localhost:5000/admin/insights', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.info = response.data.info;
      } catch (err) {
        console.error(err);
      }
    }
  
  };
  </script>
  