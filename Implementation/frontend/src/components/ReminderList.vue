<template>
    <div class="reminders-container">
               
        <div v-if="reminders.length > 0" class="reminder-list">
            <div v-for="reminder in reminders" :key="reminder._id" class="reminder-card">
                <h3>{{ reminder.type }}</h3>
                <p><strong>Date:</strong> {{ reminder.date }}</p>
                <p><strong>Notes:</strong> {{ reminder.notes || 'No notes' }}</p>
                <button @click="deleteReminder(reminder._id)" class="delete-btn">Delete</button>
            </div>
        </div>

        <p v-else class="no-reminders">No reminders found.</p>            
    </div>

</template>

<style scoped>
/* Container */
.reminders-container {
    margin-top: 22px;
    text-align: center;
}

.section-title {
    font-size: 22px;
    margin-bottom: 15px;
    color: #fdd835;
}

/* Reminder List */
.reminder-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
}


/* Reminder Card */
.reminder-card {
    background: #333;
    padding: 15px;
    border-radius: 10px;
    width: 250px;
    text-align: left;
    box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
    color: white;
}

/*Delete Button*/
.delete-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}

.delete-btn:hover {
    background-color: #a71d2a;
}   

/* No Reminders */
.no-reminders {
    color: white;
    margin-top: 20px;
}   
</style>

<script>
import { getRemindersForPet, getRemindersForOwner, deleteReminder } from '../services/reminderService.js';


export default {
    props: { petID: String },
    
    data() {
        return {
            reminders: []
        };
    },

    async mounted() {
        try {
            const ownerId = localStorage.getItem('user_id');
            if(!ownerId) {
                throw new Error("User ID not found");
            }   

            if(this.petID) {
                this.reminders = await getRemindersForPet(this.petID);
                console.log("Fetched Pet Reminders: ",this.reminders);
            } else {
                this.reminders = await getRemindersForOwner(ownerId);
                console.log("Fetched Owner Reminders: ",this.reminders);
            }  
           

        } catch (error) {
            console.error("Error fetchin reminders: ",error);
        }
    },

    async fetchReminders() {
        try {
            const ownerId = localStorage.getItem('user_id');
            if(!ownerId) {
                throw new Error("User ID not found");
            }   

           this.reminders = await getRemindersForOwner(ownerId);
           console.log("Fetched Owner Reminders: ",this.reminders);

        } catch (error) {
            console.error("Error fetchin reminders: ",error);
        }
    },

    methods: {
        async deleteReminder(reminderId) {
            try {
                await deleteReminder(reminderId);
                this.reminders = this.reminders.filter(reminder => reminder._id !== reminderId);
            } catch (error) {
                console.error("Error deleting reminder",error);
            }
        }
    }
};

</script>