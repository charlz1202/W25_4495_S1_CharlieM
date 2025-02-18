<template>
    <div class="container">
        <h1 class="title">Pet Profile</h1>

        <div v-if="pet" class="pet-details">
            <p><strong>Name: </strong>{{ pet.name }}</p>
            <p><strong>Species: </strong>{{ pet.species }}</p>
            <p><strong>Breed: </strong>{{ pet.breed || 'N/A' }}</p>
            <p><strong>Color: </strong>{{ pet.color ? pet.color : 'N/A' }}</p>
            <p><strong>Birthdate: </strong>{{ pet.dob }}</p>
            <p><strong>Age: </strong>{{ pet.age }}</p>
            <button @click="confirmDeletePet(pet._id)" class="delete-btn">Delete Pet</button>
        </div>
        
        <p v-else class="loading">Loading pet details...</p>

        <!-- Add Reminder Form-->
         <h2 class="reminder-title">Add Reminder</h2>
         <form @submit.prevent="addReminder" class="reminder-form">
             <input v-model="newReminder.date" type="date" required class="input-field" />
             <input v-model="newReminder.type" type="text" placeholder="Reminder Type (e.g. Vet Visit, Vaccine)" required class="input-field"  />
             <textarea v-model="newReminder.notes" placeholder="Notes (optional)" class="input-field"></textarea>
             <button type="submit" class="add-btn">Add Reminder</button>
        </form>

        <!-- Reminder List-->
        <h2 class="reminder-title">Reminders</h2>
        <ul v-if="reminders.length > 0" class="reminder-list">
            <li v-for="reminder in reminders" :key="reminder._id" class="reminder-item">
                <p><strong>Type: </strong>{{ reminder.type }}</p>
                <p><strong>Date: </strong>{{ reminder.date }}</p>
                <p><strong>Notes: </strong>{{ reminder.notes }}</p>
                <button @click="deleteReminder(reminder._id)" class="delete-btn">Delete</button>
            </li>
        </ul>
        <p v-else class="no-reminders">No reminders found for this pet.</p>      
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

.reminder-title {
    font-size: 24px;
    color: #fff;
}

/* Pet Details*/
.pet-details {
    background: #222;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 20px;
    text-align:left;
    
}

/* Reminder Form Styling */
.reminder-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: #444;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.iput-field {
    width: 100%;
    padding: 8px;
    border-radius: 5px;
    border: none;
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


/* Reminder List Styling */

.reminder-list {
    list-style: none;
    padding: 0;
}

.no-reminders {
    color: #f00;
}

/* Delete Button Styling */
.delete-btn {
    background-color: #f00;
    color: #fff;
    border: none;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
}

.delete-btn:hover {
    background-color: darkred;
}

/*Loading Styling */
.loading {
    color:white;
    font-size: 18px;
}

</style>



<script>
import { getPets, deletePet } from '../services/petService.js';
import { getReminders, deleteReminder, addReminder } from '../services/reminderService.js';

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
            try {
                const petId = this.$route.params.id;
                const ownerId = localStorage.getItem('user_id');
                
                if(!ownerId || !petId) {
                    throw new Error('User not logged in');
                }

                const pets = await getPets(ownerId);
                this.pet = pets.find(p => p._id === petId);

                if(!this.pet) {
                    console.error("Pet not found.");
                } else {
                    console.log('Pet details: ', this.pet);
                }
            } catch (error) {
                console.error('Error fetching pet details: ', error);
            }
        },

        async fetchReminders() {
            try {
                const ownerId = localStorage.getItem('user_id');
                if(!ownerId) {
                    throw new Error('User not logged in');
                }

                    this.reminders = await getReminders(ownerId);
                    console.log('Reminders: ', this.reminders);
                
            } catch (error) {   
                console.error('Error fetching reminders: ', error);
            }
        },

        async addNewReminder() {
            try {
                const petId = this.$route.params.id;
                const ownerId = localStorage.getItem('user_id');

                if(!ownerId || !petId) 
                    throw new Error('User not logged in');
                
                console.log('Adding reminder for pet', petId);
                
                await addReminder(localStorage.getItem("user_id"), petId, this.newReminder.date, this.newReminder.type, this.newReminder.notes);

                alert('Reminder added successfully');

                this.newReminder = {
                    date: '',
                    type: '',
                    notes: ''
                };

                await this.fetchReminders();
            } catch (error) {
                console.error('Error adding reminder: ', error);
            }
        },

        async confirmDeletePet(petId) {
            if(confirm('Are you sure you want to delete this pet?')) {
                this.deletePet();
            }
        },
  
        async deletePet() {
            try {
                await deletePet(this.pet._id);
                alert('Pet deleted successfully');  
                this.$router.push('/dashboard'); // Redisrect after deleting the pet
            } catch (error) {
                console.error('Error deleting pet: ', error);
            }
        }
    },

    async deleteReminder(reminderId) {
        try {
            await deleteReminder(reminderId);
            this.reminders = this.reminders.filter(reminder => reminder._id !== reminderId);
            alert('Reminder deleted successfully');
        } catch (error) {
            console.error('Error deleting reminder: ', error);
        }
    }
};
</script>