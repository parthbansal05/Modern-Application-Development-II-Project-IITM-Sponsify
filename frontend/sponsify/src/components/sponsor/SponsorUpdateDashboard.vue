<template>
    <div>
      <h4>{{ email }}</h4>
      <h4>{{ username }}</h4>
      <h4>{{ phno }}</h4>
      <h4>{{ industry }}</h4>

      <form @submit.prevent="updateSponsorDashboard">
            <input v-model="email" :placeholder="email" type="email"/>
            <input v-model="password" type="password" placeholder="Password" required />
            <input v-model="username" :placeholder="username" type="text" required />
            <input v-model="phno" :placeholder="phno" type="text" required />
            <select v-model="industry" :placeholder="industry" type="text" required >
              <option value="Food & Beverage">Food & Beverage</option>
              <option value="Health & Wellness">Health & Wellness</option>
              <option value="Fashion & Apparel">Fashion & Apparel</option>
              <option value="Travel & Hospitality">Travel & Hospitality</option>
              <option value="Technology & Electronics">Technology & Electronics</option>
              <option value="Education">Education</option>
              <option value="Lifestyle">Lifestyle</option>
              <option value="Gaming & Esports">Gaming & Esports</option>
              <option value="Beauty & Personal Care">Beauty & Personal Care</option>
              <option value="Finance & Banking">Finance & Banking</option>
              <option value="Parenting & Family">Parenting & Family</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Music">Music</option>
              <option value="Sports & Fitness">Sports & Fitness</option>
              <option value="Automotive">Automotive</option>
              <option value="Real Estate">Real Estate</option>
              <option value="Home & Garden">Home & Garden</option>
              <option value="Pet Care">Pet Care</option>
              <option value="Sustainability & Environment">Sustainability & Environment</option>
              <option value="Non-profit & Charity">Non-profit & Charity</option>
            </select>
            <button type="submit">Login</button>
        </form>
        <div v-if="error">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        username: '',
        phno: '',
        industry: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://localhost:5000/sponsor/update_dashboard', {
          headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
        });
        this.email = response.data.email;
        this.username = response.data.username;
        this.phno = response.data.ph_no;
        this.industry = response.data.industry;
      } catch (err) {
        this.$router.push('/login');
      }
    },
    methods: {
        async updateSponsorDashboard() {
            try {
                const response = await axios.post('http://localhost:5000/sponsor/update_dashboard', {
                  pwd: this.password,
                  username: this.username,
                  phno: this.phno,
                  industry: this.industry,
                  next: this.$route.query.next
                }, {
                  headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }
                });
                console.log(response.data);
            } catch (err) {
                this.error = 'Invalid username or password';
            }
        }
    }
  
  };
  </script>
  