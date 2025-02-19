<template>
    <div class="dashboard-container">
        <h1 class="dashboard-title">Welcome to FurBot</h1>

        <!-- Pet List -->
        <PetList />
            
        <!-- Reminders -->
        <h2 class="section-title">Upcoming Reminders</h2>
        <ReminderList />
    </div>
</template>

<script>
import PetList from "../components/PetList.vue";
import ReminderList from "../components/ReminderList.vue";

export default {
  components: {
    PetList,
    ReminderList,
  },
};  
</script>

<style scoped>
/* Dashboard  */
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

/* Titles */
.dashboard-title {
  font-size: 35px;
  margin-bottom: 35px;
    color: #fdd835;
}

.section-title {
  font-size: 22px;
  margin-top: 30px;
  color: #fdd835;
}

/* Pet List */
.pet-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

/* Pet Cards */
.pet-card {
  background: #333;
  padding: 15px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
}

.pet-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.pet-name {
  font-size: 18px;
  font-weight: bold;
  color: white;
}

/* Buttons */
.view-btn {
  display: inline-block;
  background: #007bff;
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 5px;
  margin-top: 10px;
}

.view-btn:hover {
  background: #0056b3;
}

/* Reminders */
.reminder-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reminder-card {
  background: #444;
  padding: 10px;
  border-radius: 8px;
  width: 80%;
  margin-bottom: 10px;
}

.no-reminders {
  color: #f00;
}

/* Chatbot */
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #ff9800;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.chatbot-icon {
  width: 30px;
  height: 30px;
}
</style>
