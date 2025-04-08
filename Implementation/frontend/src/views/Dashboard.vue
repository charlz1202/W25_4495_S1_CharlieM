<template>

   <!-- Logout Button -->
  <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
      <button @click="handleLogout" style="
        background-color: #ef5350;
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;">
        Logout
      </button>
    </div>

  <div class="dashboard-wrapper">
    <!-- Pet Profile & Reminders -->
    <div class="support-panel">
      <img src="/logo.jpg" alt="FurBot Logo" class="dashboard-logo" />

      <h1 class="dashboard-title">Welcome to FurBot</h1>
      <p class="subtitle">Your friendly pet assistant is ready to help!</p>


   <!-- Favorites Section -->
   <div class="card-section">
      <button class="section-toggle" @click="showFavorites = !showFavorites">
        ⭐ Saved Favorites
      </button>
      <transition name="fade">
        <div v-if="showFavorites" class="section-content">
          <FavoriteList ref="favoriteList" />
        </div>
      </transition>
    </div>

      <!-- Pet List Section -->
      <div class="card-section">
        <button class="section-toggle" @click="showPets = !showPets">
          My Pet List
        </button>
        <transition name="fade">
          <div v-if="showPets" class="section-content">
            <PetList />
          </div>
        </transition>
      </div>

      <!-- Reminders Section -->
      <div class="card-section">
        <button class="section-toggle" @click="showReminders = !showReminders">
          Upcoming Reminders
        </button>
        <transition name="fade">
          <div v-if="showReminders" class="section-content">
            <ReminderList />
          </div>
        </transition>
      </div>
    </div>

    <!-- Right: Chatbot Section -->
    <div class="chatbot-wrapper">
    <Chatbot :alwaysOpen="true" @favorite-added="handleFavoriteAdded" />
  </div>
  </div>
</template>

<script>
import Chatbot from "../components/Chatbot.vue";
import PetList from "../components/PetList.vue";
import ReminderList from "../components/ReminderList.vue";
import { logout } from "../services/authService";
import FavoriteList from "../components/FavoriteList.vue";


export default {
  components: {
    Chatbot,
    PetList,
    ReminderList,
    FavoriteList,
  },
  data() {
    return {
      showPets: true,
      showReminders: true,
      showFavorites: true,
    };
  },
  methods: {
    async handleLogout() {
      try {
        await logout();
        this.$router.push("/login");
      } catch (error) {
        console.error("Logout failed:", error);
      }
    },
  handleFavoriteAdded() {
      const favListRef = this.$refs.favoriteList;
      if (favListRef && typeof favListRef.fetchFavorites === 'function') {
        favListRef.fetchFavorites();
      }
    },
  },
  mounted() {
    // Check if user is logged in, if not redirect to login page
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
    }
  },
};
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  gap: 40px;
  padding: 40px;
  max-width: 1600px;
  margin: 0 auto;
  background-color: #f0fdf4;
  box-sizing: border-box;
  min-height: 100vh;
}

.dashboard-logo {
  width: 100px;
  height: auto;
  margin-bottom: 20px;
}

.chatbot-panel {
  flex: 1.2;
  background: #fff8e1;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chatbot-wrapper {
  background-color: #98ac9e; 
  padding: 20px;
  display: flex;
  justify-content: center;  
  align-items: start;      
  height: 100%;           
}

.support-panel {
  flex: 1.8;
  display: flex;
  flex-direction: column;
}

.dashboard-title {
  font-size: 34px;
  color: #2e7d32;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  color: #4caf50;
  margin-bottom: 25px;
}

.card-section {
  margin-top: 20px;
}

.section-toggle {
  background-color: #aed581;
  color: #2e7d32;
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 12px;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.section-toggle:hover {
  background-color: #9ccc65;
}

.section-content {
  margin-top: 10px;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 100, 0, 0.08);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>