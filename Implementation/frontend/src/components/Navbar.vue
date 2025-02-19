<template>
    <nav class="navbar">
        <div class="logo-container">
            <img src="/logo.jpg" alt="FurBot Logo" class="logo" />
            <span class="brand-name">FurBot</span>
        </div>
        <div class="auth-links">
            <router-link to="/login" v-if="!isAuthenticated">Login</router-link>
            <router-link to="/signup" v-if="!isAuthenticated">Signup</router-link>
        </div>
    </nav>
</template>

<style scoped>
/* Navbar Styling */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #333;
    color: white;
}
.logo-container {
    display: flex;
    align-items: center;
}

.log {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
}

.brand-name {
    font-size: 24px;
    font-weight: bold;
    color:white;
}

.auth-links {
    display: flex;
    gap: 20px;
}   

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}   

.nav-link:hover {
    color: #007bff;
}

</style>