<template>
    <div>
      <h4>{{ campaign }}</h4>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        campaign: "",
        id: this.$route.params.id
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/view_campaigns/' + this.id, {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.campaign = response.data.campaign;
      } catch (err) {
        console.error(err);
      }
    }
  };
  </script>
  