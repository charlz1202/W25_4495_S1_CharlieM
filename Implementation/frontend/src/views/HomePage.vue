<template>
    <div class="home-container">
      <div class="card">
        <img src="/logo.jpg" alt="FurBot Logo" class="logo" />
        <h1 class="brand">FurBot</h1>
        <p class="tagline">Your friendly pet assistant</p>
  
        <nav class="nav-links">
          <router-link to="/login" class="nav-btn">🐾 Login</router-link>
          <router-link to="/signup" class="nav-btn">📝 Signup</router-link>
        </nav>
      </div>
    </div>
  </template>
  
  <style scoped>
  /*
  .home-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(to right, #e8f5e9, #d0f0c0);
  }*/
  
  .card {
    background-color: white;
    padding: 40px 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 100, 0, 0.15);
    width: 360px;
  }
  
  .logo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 12px;
  }
  
  .brand {
    font-size: 36px;
    font-weight: bold;
    color: #2e7d32;
    margin: 0;
  }
  
  .tagline {
    font-size: 16px;
    color: #4caf50;
    margin-top: 6px;
    margin-bottom: 24px;
  }
  
  .nav-links {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .nav-btn {
    background-color: #4caf50;
    color: white;
    text-decoration: none;
    font-size: 18px;
    padding: 12px;
    border-radius: 10px;
    font-weight: bold;
    transition: background 0.3s;
  }
  
  .nav-btn:hover {
    background-color: #388e3c;
  }
  </style>  