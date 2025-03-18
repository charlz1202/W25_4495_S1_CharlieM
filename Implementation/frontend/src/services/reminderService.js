import axios from "axios";

const API_URL = "http://127.0.0.1:5000"; // Flask API

export const addReminder = async (ownerId, petId, date, type, notes) => {
    try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("User not authenticated. Please log in.");
        if (!ownerId || !petId || !date) throw new Error("Missing required fields for reminder.");

        // Fix date YYYY-MM-DD format
        const datePattern = /^\d{4}-\d{2}-\d{2}$/;
        if (!datePattern.test(date)) throw new Error("Invalid date format. Use YYYY-MM-DD.");

        const payload = { owner_id: ownerId, pet_id: petId, date, type, notes };
        console.log("Sending Reminder:", JSON.stringify(payload, null, 2));

        const response = await axios.post(`${API_URL}/reminders`, payload, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        console.log("Reminder Added:", response.data);
        return response.data;
    } catch (error) {
        console.error("Add Reminder Error:", error);
        throw error.response?.data?.error || "Failed to add reminder";
    }
};

//Get Reminders for pets
export const getRemindersForPet = async (petId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_URL}/reminders/${petId}`, {
            headers: { Authorization: `Bearer ${token}` },
        });

        console.log("Reminders Response (Pet):", response.data);
        return response.data;
    } catch (error) {
        console.error("Get Reminders Error:", error.response?.data || "No Response");
        throw error.response?.data?.error || "Failed to fetch reminders for pet";
    }
};

// Get Reminders for owner
export const getRemindersForOwner = async (ownerId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_URL}/reminders/owner/${ownerId}`, {
            headers: { Authorization: `Bearer ${token}` },
        });

        console.log("Reminders Response (Owner):", response.data);
        return response.data;
    } catch (error) {
        console.error("Get Reminders Error:", error.response?.data || "No Response");
        throw error.response?.data?.error || "Failed to fetch reminders for owner";
    }
};


export const deleteReminder = async (reminderId) => {
    try {
        const token = localStorage.getItem("token");
        console.log(`Deleting Reminder with ID: ${reminderId}`);

        const response = await axios.delete(`${API_URL}/reminders/${reminderId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        console.log("Reminder Deleted:", response.data);
        return response.data;
    } catch (error) {
        console.error("Delete Reminder Error:", error.response?.data || "No Response");
        throw error.response?.data?.error || "Failed to delete reminder";
    }
};