<template>
    <div class="container">
        <h1 class="title">My Pets</h1>
        
        <!-- Add a form to add a new pet -->
        <form @submit.prevent="addNewPet" class="pet-form">
            <input v-model="name" type="text" placeholder="Pet Name" required />
            <input v-model="species" type="text" placeholder="Species" required />
            <input v-model="dob" type="date" required />
            <input v-model="color" type="text" placeholder="Color" />
            <input v-model="breed" type="text" placeholder="Breed" />
            <button type="submit">Add Pet</button>
        </form>

        <!-- Display a list of pets -->
         <h3 class="list-title">My Pet list</h3>
         <ul v-if="pets.length > 0" class ="pet-list">
             <li v-for="pet in pets" :key="String(pet._id)" class="pet-item">
                 <router-link :to="{ name: 'PetProfile', params: { id: pet._id }}" class="pet-name">
                     {{ pet.name }}
                 </router-link>
                 <button @click="deletePet(pet._id)" class="delete-btn">Delete</button>
             </li>
         </ul>
         <p v-else class="no-pets">No pets found.</p>
    </div>
</template>

<style scoped>
/* Container Styling */
.container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}

/* Title Styling */
.title {
    font-size: 28px;
    color: #fff;
}

/* Form Styling */
.pet-form {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
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
.list-style {
   font-size: 20px;
   color: white;
   margin-bottom: 10px;
}

.pet-list {
    list-style-type: none;
    padding: 0;
    margin: 10px 0;
}

.pet-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    padding: 10px;
    border-radius: 5px solid #ccc;
    margin-bottom: 10px;
}

.pet-name {
    flex-grow: 1;
}

.delete-btn {
    background-color: red;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor:pointer;
}

.delete-btn:hover {
    background-color: darkred;
}

/* No Pets Found Styling */
.no-pets {
    color: white;
    font-size: 18px;
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