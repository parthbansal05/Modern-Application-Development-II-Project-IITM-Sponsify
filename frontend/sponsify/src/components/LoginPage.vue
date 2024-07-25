<template>
    <div class="login-container" >
        <div v-if="error" class="error-message">
            {{ error }}
     
            <button @click="closeError" class = "close-btn">
                &nbsp; &times; &nbsp;
            </button>
   
        </div>
     
        <form @submit.prevent="login" class="login-form">
            <input v-model="email" placeholder="Email" type="email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            email: '',
            password: '',
            error: '',
            // bg_img: require('@/assets/background.jpeg')
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
                this.error = 'Invalid Username or Password !';
            }
        },

        closeError() {
                this.error = '';
        }
    }
};
</script>

<style scoped>
.error-message{
    display: flex;
    width: 30rem;
    align-items: center;
    justify-content: space-between;
    font-size: 1.2rem;
    background: rgba(255, 107, 107, 0.8);
    color: rgb(188, 0, 0);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 8px;
}

.close-btn {
  position: relative;
  top: 0px;
  right: 10px;
  background: none;
  border: none;
  border-radius: 2px; 
  font-size: 2rem;
  cursor: pointer;
  color: rgb(188, 0, 0);
  padding: 0rem; 
}
.close-btn:hover {
    color: darkred;
}

.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #FFFFFF;
    background-image: url('@/assets/background.jpeg'); /* Replace with your image path */
    background-size: cover; /* Adjust this to cover, contain, or other values based on your need */
    background-position: center; /* Adjust the position as needed */
    background-repeat: no-repeat; /* Ensure the image doesn't repeat */
}

.login-form {
    display: flex;
    width: 30rem;
    flex-direction: column;
    background: white;
    padding: 1.5rem;
    padding-top: 15rem;
    border-radius: 8px;

    
    position: relative;
    z-index: 2;
    
    background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 20%, rgba(255, 255, 255, 0.2) 40%, rgba(255, 255, 255, 0.8) 60%),url('@/assets/leafy_bg.jpeg');
    background-size: cover;
    

}

.login-form input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    font-size: 1rem;
    background-color: #FFFFFF;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.login-form button {
    padding: 0.5rem;
    font-size: 1rem;
    color: white;
    background-color: #38566E;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.login-form button:hover {
    background-color: #B97A57;
}


</style>