<template>
  <div>
      <form @submit.prevent="login">
          <input type="text" v-model="campTitle" placeholder="Campaign Title" required>
          <input type="text" v-model="campDesc" placeholder="Campaign Description" required>
          <input type="date" v-model="startDate" placeholder="Start Date" required>
          <input type="date" v-model="endDate" placeholder="End Date" required>
          <input type="number" v-model="budget" placeholder="Budget" required>
            <select v-model="visibility" required>
              <option value="public">Public</option>
              <option value="private">Private</option>
            </select>
          <input type="text" v-model="goal" placeholder="Goal" required>
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
          campTitle: '',
          campDesc: '',
          startDate: '',
          endDate: '',
          budget: '',
          visibility: 'public',
          goal: '',
          error: ''
      };
  },
  methods: {
      async login() {
          try {
              const response = await axios.post('http://localhost:5000/sponsor/create_campaign', {
                  campTitle: this.campTitle,
                  campDesc: this.campDesc,
                  startDate: this.startDate,
                  endDate: this.endDate,
                  budget: this.budget,
                  visibility: this.visibility,
                  goal: this.goal,
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