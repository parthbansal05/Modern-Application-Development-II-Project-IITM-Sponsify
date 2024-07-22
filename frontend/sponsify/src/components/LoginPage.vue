<template>
    <div>
        <form @submit.prevent="login">
            <input v-model="email" placeholder="Email" type="email" required />
            <input v-model="password" type="password" placeholder="Password" required />
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
            password: '',
            error: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://localhost:5000/login', {
                    email: this.email,
                    pwd: this.password,
                    next: this.$route.query.next
                });
                console.log(response.data);
                sessionStorage.setItem('token', response.data.access_token);
                const nextUrl = response.data.redirect_url || '/';
                this.$router.push(nextUrl);
            } catch (err) {
                this.error = 'Invalid username or password';
            }
        }
    }
};
</script>