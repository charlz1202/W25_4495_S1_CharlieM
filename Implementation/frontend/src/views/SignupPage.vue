<template>
  <div class="signup-wrapper">
    <div class="signup-container">
      <h2 class="signup-title">Create Your Account</h2>
      <form @submit.prevent="handleSignup" class="signup-form">
        <input
          v-model="email"
          type="email"
          placeholder="Enter your email"
          required
          class="input-field"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Create a password"
          required
          class="input-field"
        />
        <button type="submit" class="signup-btn">Sign Up</button>
      </form>
      <p class="logic-link">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { signup } from "../services/authService.js";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleSignup() {
      try {
        const response = await signup(this.email, this.password);

        alert(response.message || "Signup successful!");

        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = error.message || "An error occurred during signup.";
        alert(this.errorMessage);
      }
    },
  },
};
</script>

<style scoped>
.signup-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to right, #e0f2f1, #a5d6a7);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.signup-container {
  background: white;
  padding: 40px 30px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

.signup-title {
  margin-bottom: 25px;
  color: #2e7d32;
}

.input-field {
  padding: 12px;
  margin: 10px 0;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  font-size: 14px;
}

.signup-btn {
  margin-top: 15px;
  padding: 12px;
  width: 100%;
  background: #66bb6a;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.signup-btn:hover {
  background: #388e3c;
}

.logic-link {
  margin-top: 15px;
  font-size: 14px;
}

.logic-link a {
  color: #2e7d32;
  text-decoration: none;
  font-weight: bold;
}
</style>