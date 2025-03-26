<template>
    <div class="pet-profile-page">
      <h1 class="title">🐾 Pet Profile</h1>
  
      <!-- Pet Info Card -->
      <div v-if="pet" class="pet-card full-width">
        <div class="emoji">
          <span v-if="pet.species.toLowerCase() === 'dog'">🐶</span>
          <span v-else-if="pet.species.toLowerCase() === 'cat'">🐱</span>
          <span v-else>🐾</span>
        </div>
        <h2 class="pet-name">{{ pet.name }}</h2>
        <ul class="pet-info">
          <li><strong>Species:</strong> {{ pet.species }}</li>
          <li><strong>Breed:</strong> {{ pet.breed || 'N/A' }}</li>
          <li><strong>Color:</strong> {{ pet.color || 'N/A' }}</li>
          <li><strong>Birthdate:</strong> {{ pet.dob }}</li>
          <li><strong>Age:</strong> {{ pet.age }}</li>
        </ul>
        <button @click="confirmDeletePet(pet._id)" class="delete-btn">Delete Pet</button>
      </div>
      <p v-else class="loading">Loading pet details...</p>
  
      <!-- Form + Reminders Layout -->
      <div class="content-columns">
        <div class="form-section">
          <h2 class="section-title">➕ Add Reminder</h2>
          <form @submit.prevent="addNewReminder" class="reminder-form">
            <input v-model="newReminder.date" type="date" required />
            <input v-model="newReminder.type" type="text" placeholder="Reminder Type (e.g. Vet Visit, Vaccine)" required />
            <textarea v-model="newReminder.notes" placeholder="Notes (optional)"></textarea>
            <button type="submit" class="add-btn">Add Reminder</button>
          </form>
        </div>
  
        <div class="reminders-section">
          <h2 class="section-title">📅 Reminders</h2>
          <ul v-if="reminders.length" class="reminder-list">
            <li v-for="reminder in reminders" :key="reminder._id" class="reminder-item">
              <p><strong>Type:</strong> {{ reminder.type }}</p>
              <p><strong>Date:</strong> {{ reminder.date }}</p>
              <p><strong>Notes:</strong> {{ reminder.notes || 'None' }}</p>
              <button @click="deleteReminder(reminder._id)" class="delete-btn">Delete</button>
            </li>
          </ul>
          <p v-else class="no-reminders">No reminders found for this pet.</p>
        </div>
      </div>
  
      <button @click="goToDashboard" class="back-btn">⬅ Back to Dashboard</button>
    </div>
  </template>
  
  <script>
  import { getPets, deletePet } from '../services/petService.js';
  import { getRemindersForPet, deleteReminder, addReminder } from '../services/reminderService.js';
  
  export default {
    data() {
      return {
        pet: null,
        reminders: [],
        newReminder: {
          date: '',
          type: '',
          notes: ''
        }
      };
    },
    async mounted() {
      await this.fetchPetDetails();
      await this.fetchReminders();
    },
    methods: {
      async fetchPetDetails() {
        const petId = this.$route.params.id;
        const ownerId = localStorage.getItem('user_id');
        if (!ownerId || !petId) return;
        const pets = await getPets(ownerId);
        this.pet = pets.find(p => p._id === petId);
      },
      async fetchReminders() {
        const petId = this.$route.params.id;
        if (petId) {
          this.reminders = await getRemindersForPet(petId);
        }
      },
      async addNewReminder() {
        const petId = this.$route.params.id;
        const ownerId = localStorage.getItem('user_id');
        await addReminder(ownerId, petId, this.newReminder.date, this.newReminder.type, this.newReminder.notes);
        this.newReminder = { date: '', type: '', notes: '' };
        await this.fetchReminders();
      },
      async confirmDeletePet(petId) {
        if (confirm('Are you sure you want to delete this pet?')) {
          await deletePet(petId);
          this.$router.push('/dashboard');
        }
      },
      async deleteReminder(reminderId) {
        await deleteReminder(reminderId);
        this.reminders = this.reminders.filter(r => r._id !== reminderId);
      },
      goToDashboard() {
        this.$router.push('/dashboard');
      }
    }
  };
  </script>
  
  <style scoped>
  .pet-profile-page {
    max-width: 1000px;
    margin: 0 auto;
    background: #f5f5f5;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .title {
    text-align: center;
    font-size: 32px;
    margin-bottom: 20px;
    color: #2e7d32;
  }
  
  .full-width {
    width: 100%;
    margin-bottom: 30px;
  }
  
  .pet-card {
    background: #fff;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  }
  
  .emoji {
    font-size: 48px;
    margin-bottom: 10px;
  }
  
  .pet-name {
    font-size: 24px;
    color: #4caf50;
    margin-bottom: 10px;
  }
  
  .pet-info {
    list-style: none;
    padding: 0;
    color: #333;
    font-size: 16px;
    text-align: left;
    max-width: 300px;
    margin: 0 auto;
  }
  
  .content-columns {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .form-section,
  .reminders-section {
    flex: 1;
    min-width: 300px;
  }
  
  .section-title {
    font-size: 22px;
    margin: 20px 0 10px;
    color: #2e7d32;
  }
  
  .reminder-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: #e8f5e9;
    padding: 20px;
    border-radius: 10px;
  }
  
  .reminder-form input,
  .reminder-form textarea {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 14px;
  }
  
  .add-btn {
    background-color: #4caf50;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
  }
  
  .add-btn:hover {
    background-color: #388e3c;
  }
  
  .reminder-list {
    padding: 0;
    list-style: none;
  }
  
  .reminder-item {
    background: #565756;
    color: white;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    text-align: left;
  }
  
  .delete-btn {
    margin-top: 10px;
    background-color: #f44336;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
  }
  
  .delete-btn:hover {
    background-color: #c62828;
  }
  
  .no-reminders {
    text-align: center;
    color: #777;
  }
  
  .back-btn {
    display: block;
    margin: 30px auto 0;
    padding: 12px 24px;
    font-size: 16px;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  
  .back-btn:hover {
    background-color: #1976d2;
  }
  </style>