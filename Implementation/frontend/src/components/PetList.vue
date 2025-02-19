<template>
    <div class="container">
        <h3 class="title">Add a new pet</h3>
        
        <!-- Form to add a new pet -->
        <form @submit.prevent="addNewPet" class="pet-form">
            <input v-model="name" type="text" placeholder="Pet Name" required />
            <input v-model="species" type="text" placeholder="Species" required />
            <input v-model="dob" type="date" required />
            <input v-model="color" type="text" placeholder="Color" />
            <input v-model="breed" type="text" placeholder="Breed" />
            <button type="submit">Add Pet</button>
        </form>

        <!-- Display a list of pets -->
        <h2 class="list-title">My Pet List</h2>
        <div v-if="pets.length > 0" class="pet-list">
            <div v-for="pet in pets" :key="String(pet._id)" class="pet-card">
                <img src="/pet-placeholder.jpg" alt="Pet" class="pet-image" />
                <h3 class="pet-name">{{ pet.name }}</h3>
                <p><strong>Species:</strong> {{ pet.species }}</p>
                <p><strong>Breed:</strong> {{ pet.breed || 'N/A' }}</p>
                <p><strong>Color:</strong> {{ pet.color || 'N/A' }}</p>
                <p><strong>Age:</strong> {{ pet.age }}</p>

                <div class="card-actions">
                    <router-link :to="{ name: 'PetProfile', params: { id: pet._id }}" class="view-profile">
                        View Profile
                    </router-link>
                    <button @click="deletePet(pet._id)" class="delete-btn">Delete</button>
                </div>
            </div>
        </div>
        <p v-else class="no-pets">No pets found.</p>
    </div>
</template>


<style scoped>
/* Container Styling */
.container {
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
}

/* Title Styling */
.title {
    font-size: 20px;
    color: #fff;
}

/* List Title */
.list-title {
    font-size: 30px;
    color: #fff;
    margin-top: 30px;
}

/* Form Styling */
.pet-form {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 50px
}

.pet-form input {
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
    width: 100%;
    max-width: 200px;
}

/* Add Button */

.add-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}

.add-btn:hover {
    background-color: #0056b3;
}

/* Pet List Styling */
.pet-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    justify-content: center;
    padding: 20px;
}

.pet-card {
    background-color: #333;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
    transition: transform 0.2s ease-in-out;
}

.pet-card:hover {
    transform: scale(1.05);
}

/* Pet Image */
.pet-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 10px;
}

/* Pet Name */
.pet-name {
    font-size: 20px;
    font-weight: bold;
    color: #fdd835;
}

/* Card Actions */
.card-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 10px;
}

.view-profile {
    background-color: #28a745;
    color: white;
    text-decoration: none;
    padding: 8px 12px;
    border-radius: 5px;
    font-size: 14px;
    transition: 0.3s;
}

.view-profile:hover {
    background-color: #218838;
}

.delete-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    transition: 0.3s;
}

.delete-btn:hover {
    background-color: #c82333;
}

/* No Pets Message */
.no-pets {
    font-size: 18px;
    color: #fff;
    margin-top: 20px;
}   

</style>

<script>
import { addPet, getPets, deletePet } from '../services/petService.js';

export default {
    data() {
        return {
            pets: [],
            name: '',
            species: '',
            dob: '',
            color: '',
            breed: '',
            ownerId: localStorage.getItem("user_id") || ""
        };  
    },

    async mounted() {
        await this.fetchPets();
    },

    // Methods to add a new pet and delete a pet

    methods: {
        async fetchPets() {
            try {
                const ownerId = localStorage.getItem('user_id');
                if(!ownerId) {
                    throw new Error('User not logged in');
                }
                this.pets = await getPets(ownerId);
            } catch (error) {
                console.error('Error fetching pets: ', error);
            }
        },
    
        async addNewPet() {
            try {
                if(!this.ownerId) {
                    throw new Error('User not logged in. Cannot add pet');
                }

                console.log("Adding pet for owner: ", this.ownerId);

                await addPet(
                    this.ownerId,
                    this.name,
                    this.species,
                    this.dob,
                    this.color,
                    this.breed
                );

                this.name = '';
                this.species = '';
                this.dob = '';
                this.color = '';
                this.breed = '';

                alert('Pet added successfully');
                await this.fetchPets();
            } catch (error) {
                console.error("Error adding pet: ", error);
                alert("Failed to add pet");
            }
        },

    
        async deletePet(petId) {
            try {
                console.log('Deleting pet: ', petId);
                await deletePet(petId);
                this.pets = this.pets.filter(pet => pet._id !== petId);
            } catch (error) {
                console.error('Error deleting pet: ', error);
            }
        }
    }
};

</script>