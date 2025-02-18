<template>
    <div>
        <h2>Reminders</h2>
        <ul v-if="reminders.length > 0">
            <li v-for="reminder in reminders" :key="reminder._id">
                <p><strong>Type:</strong> {{ reminder.type }}</p>
                <p><strong>Date:</strong> {{ reminder.date }}</p>
                <p><strong>Notes:</strong> {{ reminder.notes }}</p>
                <button @click="deleteReminder(reminder._id)">Delete</button>
            </li>
        </ul>
        <p v-else>No reminders found.</p>            
    </div>
</template>

<script>
import { getReminders, deleteReminder } from '../services/reminderService';

export default {
    data() {
        return {
            reminders: []
        };
    },

    async mounted() {
        try {
            const ownerId = localStorage.getItem('user_id');
            this.reminders = await this.getReminders();
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