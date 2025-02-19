<template>
    <div class="home-container">
      <div class="card">
        <img src="/logo.jpg" alt="FurBot Logo" class="logo" />
        <h1 class="brand">FurBot</h1>
        <nav class="nav-links">
          <router-link to="/login" class="nav-btn">Login</router-link>
          <router-link to="/signup" class="nav-btn">Signup</router-link>
        </nav>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* Center  */
  .home-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #222;
  }
  
  /* Card style */
  .card {
      background-color: #333;
      padding: 30px;
      border-radius: 12px;
      text-align: center;
      box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
      width: 320px;
  }
  
  /* Logo & App Name */
  .logo {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 10px;
  }
  
  .brand {
      font-size: 32px;
      font-weight: bold;
      color: white;
  }
  
  /* Navigation Buttons */
  .nav-links {
      display: flex;
      flex-direction: column;
      gap: 15px;
      margin-top: 20px;
  }
  
  .nav-btn {
      background-color: #007bff;
      color: white;
      text-decoration: none;
      font-size: 18px;
      padding: 12px;
      border-radius: 5px;
      display: inline-block;
      transition: 0.3s;
      text-align: center;
  }
  
  .nav-btn:hover {
      background-color: #0056b3;
  }
  </style>
  