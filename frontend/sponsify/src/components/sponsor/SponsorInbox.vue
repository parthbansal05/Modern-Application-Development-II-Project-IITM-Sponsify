<template>
    <div>
      <h4>{{ inbox }}</h4>
      <h4>{{ camp_dict }}</h4>
      <h4>{{ influencer }}</h4>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        inbox: '',
        camp_dict: '',
        influencer: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/inbox', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.inbox = response.data.inbox;
        this.camp_dict = response.data.camp_dict;
        this.influencer = response.data.influencer;
      } catch (err) {
        console.log(err);
      }
    }
  
  };
  </script>
  