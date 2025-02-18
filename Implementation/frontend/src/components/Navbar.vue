<template>
    <nav>
        <router-link to="/dashboard">Dashboard</router-link>
        <button @click="logout">Logout</button>
    </nav>
</template>

<script>
import { logout } from '../services/authService';

export default {
    methods: {
        logout() {
            logout();
            this.$router.push('/login');
        }
    }
};
</script>

<style>
    nav {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background: #333;
        color: white;
    }   
    a {
        color: white;
        text-decoration: none;
        margin-right: 10px;
    }

    button {
        background:red;
        color: white;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
    }
</style>