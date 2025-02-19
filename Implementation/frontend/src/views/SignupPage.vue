<template>
  <div class="signup-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="handleSignup" class="signup-form">
      <input v-model="email" type="email" placeholder="Email" required class="input-field" />
      <input v-model="password" type="password" placeholder="Password" required class="input-field" />
      <button type="submit" class="signup-btn">Sign Up</button>
    </form>

    <p class="logic-link">Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
import { signup } from "../services/authService.js";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },

  methods: {
    async handleSignup() {
      try {
        const response = await signup(this.email, this.password);
        alert(response.message);
        this.$router.push("/login"); // Redirect to login page
      } catch (error) {
        this.errorMessage = error;
      }
    },
  },
};
</script>

<style scoped>

.signup-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  background: #222;
  border-radius: 10px;
}

.input-field {
  padding: 8px;
  margin: 10px 0;
  width: 100%;
  max-width: 300px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.signup-btn {
  padding: 8px;
  width: 100%;
  max-width: 300px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.signup-btn:hover {
  background: #0056b3;
}

.login-link {
  color: #007bff;
  text-decoration: none;
} 

</style>