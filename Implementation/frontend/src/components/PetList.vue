<template>
    <div class="container">
      <!-- Add Pet Form -->
      <h3 class="title">🐾 Add a New Pet</h3>
  
      <form @submit.prevent="addNewPet" class="pet-form">
        <input v-model="name" type="text" placeholder="Pet Name" required />
        <input v-model="species" type="text" placeholder="Species" required />
        <input v-model="dob" type="date" required />
        <input v-model="color" type="text" placeholder="Color" />
        <input v-model="breed" type="text" placeholder="Breed" />
        <button type="submit" class="add-btn">Add Pet</button>
      </form>
  
      <!-- Filter Section -->
      <div class="filter-section">
        <label for="species-filter">Filter:</label>
        <select id="species-filter" v-model="speciesFilter">
          <option value="">All Pets</option>
          <option value="Dog">Show Dogs Only</option>
          <option value="Cat">Show Cats Only</option>
        </select>
      </div>
  
      <!-- Pet List -->
      <h2 class="list-title">🐾 My Pet List</h2>
      <transition-group name="fade" tag="div" class="pet-list">
        <div
          v-for="pet in filteredPets"
          :key="String(pet._id)"
          class="pet-card"
        >
        <div class="pet-icon">
        {{ pet.species.toLowerCase().includes("cat") ? "🐱" : "🐶" }}
        </div>
          <h3 class="pet-name">
            {{ pet.name }}
          </h3>
          <p><strong>Species:</strong> {{ pet.species }}</p>
          <p><strong>Breed:</strong> {{ pet.breed || "N/A" }}</p>
          <p><strong>Color:</strong> {{ pet.color || "N/A" }}</p>
          <p><strong>Age:</strong> {{ pet.age }}</p>
  
          <div class="card-actions">
            <router-link
              :to="{ name: 'PetProfile', params: { id: pet._id } }"
              class="view-profile"
            >
              View Profile
            </router-link>
            <button @click="deletePet(pet._id)" class="delete-btn">Delete</button>
          </div>
        </div>
      </transition-group>
  
      <p v-if="filteredPets.length === 0" class="no-pets">No pets found.</p>
    </div>
  </template>
  
  <script>
  import { addPet, getPets, deletePet } from "../services/petService.js";
  
  export default {
    data() {
      return {
        pets: [],
        name: "",
        species: "",
        dob: "",
        color: "",
        breed: "",
        ownerId: localStorage.getItem("user_id") || "",
        speciesFilter: "",
      };
    },
  
    async mounted() {
      await this.fetchPets();
    },
  
    computed: {
      filteredPets() {
        if (!this.speciesFilter) return this.pets;
        return this.pets.filter(
          (pet) =>
            pet.species &&
            pet.species.toLowerCase() === this.speciesFilter.toLowerCase()
        );
      },
    },
  
    methods: {
      // Fetches the list of pets
      async fetchPets() {
        try {
          const ownerId = localStorage.getItem("user_id");
          if (!ownerId) throw new Error("User not logged in");
          this.pets = await getPets(ownerId);
        } catch (error) {
          console.error("Error fetching pets: ", error);
        }
      },
  
      // addNewPet method is called when the form is submitted
      async addNewPet() {
        try {
          if (!this.ownerId) throw new Error("User not logged in");
          
          // Trigger the addPet function from petService.js to add a new pet passing the required parameters
          await addPet(
            this.ownerId,
            this.name,
            this.species,
            this.dob,
            this.color,
            this.breed
          );
  
          // Reset the form fields after successful addition of pet
          this.name = "";
          this.species = "";
          this.dob = "";
          this.color = "";
          this.breed = "";
  
          alert("Pet added successfully"); // Show success message
          await this.fetchPets(); // Fetch the updated list of pets
        } catch (error) {
          console.error("Error adding pet: ", error);
          alert("Failed to add pet");
        }
      },
  
      async deletePet(petId) {
        try {
          await deletePet(petId);
          this.pets = this.pets.filter((pet) => pet._id !== petId);
        } catch (error) {
          console.error("Error deleting pet: ", error);
        }
      },
  
      getPetEmoji(species) {
        if (!species) return "🐾";
        const lower = species.toLowerCase();
        if (lower.includes("dog")) return "🐶";
        if (lower.includes("cat")) return "🐱";
        return "🐾";
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
    font-family: "Segoe UI", sans-serif;
  }
  
  /* Titles */
  .title {
    font-size: 24px;
    color: #2e7d32;
    margin: 25px 0 15px;
    font-weight: bold;
  }
  
  .list-title {
    font-size: 28px;
    color: #2e7d32;
    margin-top: 40px;
    font-weight: bold;
  }
  
  /* Form */
  .pet-form {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-bottom: 30px;
  }
  
  .pet-form input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #a7a9a7;
  color: #fafefa;
  width: 100%;
  max-width: 180px;
  font-size: 14px;
}
  
  .add-btn {
    background-color: #66bb6a;
    color: white;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 15px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .add-btn:hover {
    background-color: #4caf50;
  }
  
  /* Filter */
  .filter-section {
    margin-bottom: 20px;
  }
  
  .filter-section label {
    margin-right: 10px;
    font-weight: 500;
    color: #2e7d32;
  }
  
  .filter-section select {
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #ccc;
  }
  
  /* Pet List */
  .pet-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    padding: 20px;
  }
  
  /* Pet Card */
  .pet-card {
    background-color: #ffffff;
    padding: 16px 12px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(34, 139, 34, 0.1);
    transition: transform 0.2s ease-in-out;
    min-height: 0px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
  }
  
  .pet-card:hover {
    transform: scale(1.03);
  }
  
  .pet-icon {
    font-size: 70px;
    margin-bottom: 10px;
  } 
  .pet-name {
    font-size: 20px;
    font-weight: bold;
    color: #f9a825;
    margin-bottom: 6px;
  }
  
  /* Actions */
  .card-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 10px;
  }
  
  .view-profile {
    background-color: #43a047;
    color: white;
    text-decoration: none;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 14px;
    transition: 0.3s;
  }
  
  .view-profile:hover {
    background-color: #388e3c;
  }
  
  .delete-btn {
    background-color: #ef5350;
    color: white;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: 0.3s;
  }
  
  .delete-btn:hover {
    background-color: #d32f2f;
  }
  
  /* No Pets Message */
  .no-pets {
    font-size: 18px;
    color: #888;
    margin-top: 20px;
  }
  
  /* Animations */
  .fade-enter-active,
  .fade-leave-active {
    transition: all 0.5s ease;
  }
  .fade-enter-from {
    opacity: 0;
    transform: translateY(15px);
  }
  .fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  </style>  