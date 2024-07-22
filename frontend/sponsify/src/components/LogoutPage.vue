<template>
    <div>
        <button @click="logout">Logout</button>
    </div>
</template>

<script>
export default {
    methods: {
        logout() {
            sessionStorage.removeItem('token');  // Change to sessionStorage
            this.$router.push('/login');
        }
    }
};
</script>