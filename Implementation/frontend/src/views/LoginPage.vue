<template>
  <div class="login-container">
    <div class="login-card">
      <img src="/logo.jpg" alt="FurBot Logo" class="logo" />
      <h1 class="title">Welcome Back to FurBot</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from "../services/authService";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await login(this.email, this.password);
        localStorage.setItem("token", response.token);
        localStorage.setItem("user_id", response.user_id);
        this.$router.push("/dashboard");
      } catch (error) {
        this.errorMessage = "Login failed. Please check your credentials.";
      }
    },
  },
};
</script>

<style scoped>

.logo {
  width: 100px;
  max-width: 80%;
  display: block;
  margin: 0 auto 20px auto;
}

.login-card {
  background: #ffffff;
  padding: 40px 30px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 100, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #2e7d32;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.login-form input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  color: #f3f0f0;
  background: #707170;
}

.login-form button {
  background-color: #4caf50;
  color: white;
  padding: 12px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.login-form button:hover {
  background-color: #388e3c;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}

.login-form input::placeholder {
  color: white;
  opacity: 1;
}

</style>
