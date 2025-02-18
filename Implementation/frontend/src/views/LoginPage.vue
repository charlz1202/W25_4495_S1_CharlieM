<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
          this.errorMessage = error;
        }
      }
    }
  };
</script>

<style scoped>
.error {
     color: red;
}
    </style>