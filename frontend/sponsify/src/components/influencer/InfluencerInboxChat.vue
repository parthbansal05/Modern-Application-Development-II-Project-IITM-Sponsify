<template>
  <div>
    <h4>{{ inbox }}</h4>
    <h4>{{ camp_dict }}</h4>
    <h4>{{ sponsor }}</h4>

    <form @submit.prevent="sendMsg">
            <input v-model="msg" :placeholder="msg" type="text"/>
            <input v-model="modified_budget" :placeholder="modified_budget" type="number"/>
            <input v-model="modified_terms" :placeholder="modified_terms" type="text"/>
            <select v-model="campain_id" :placeholder="campain_id" type="text" required >
              <option value="Food & Beverage">Food & Beverage</option>
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
      inbox: '',
      camp_dict: '',
      sponsor: '',
      msg: '',
      campain_id: '',
      modified_budget: '',
      modified_terms: '',
      id: this.$route.params.id
    };
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:5000/influencer/inbox/' + this.id, {
        headers: { Authorization: `Bearer ${sessionStorage.getItem('token')}` }  // Change to sessionStorage
      });
      this.inbox = response.data.inbox;
      this.camp_dict = response.data.camp_dict;
      this.sponsor = response.data.sponsor;
    } catch (err) {
      console.log(err);
    }
  },
    methods: {
        async sendMsg() {
            try {
                const response = await axios.post('http://localhost:5000/influencer/inbox/' + this.id, {
                  msg: this.msg,
                  campain_id: this.campain_id,
                  modified_budget: this.modified_budget,
                  modified_terms: this.modified_terms,
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
