<template>
    <div>
        <h1>Logging out...</h1>
    </div>
</template>

<script>
export default {
    async created() {
        sessionStorage.removeItem('token');  // Change to sessionStorage
        this.$router.push('/login');
    }
};
</script>