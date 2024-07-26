<template>
    <div>
      <h1>Current User: {{ inbox }}</h1>
      <h1>Current User: {{ camp_dict }}</h1>
      <h1>Current User: {{ sponsors }}</h1>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        inbox: [],
        camp_dict: {},
        sponsors: []
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/influencer/inbox', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.inbox = response.data.inbox;
        this.camp_dict = response.data.camp_dict;
        this.sponsors = response.data.sponsors;
      } catch (err) {
        this.$router.push('/login');
      }
    }
  
  };
  </script>
  