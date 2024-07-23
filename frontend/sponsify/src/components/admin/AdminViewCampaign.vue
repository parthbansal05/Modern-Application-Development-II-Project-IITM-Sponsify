<template>
    <div>
      <h4>{{ campaign }}</h4>
      <h4>{{ sponsors }}</h4>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        campaign: "",
        sponsors: "",
        id: this.$route.params.id
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/admin/view_campaign/' + this.id, {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.campaign = response.data.campaign;
        this.sponsors = response.data.sponsors;
      } catch (err) {
        console.error(err);
      }
    }
  
  };
  </script>
  