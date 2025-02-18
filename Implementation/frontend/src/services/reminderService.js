import axios from "axios";

const API_URL = 'http://127.0.0.1:5000'; // Flask API

export const addReminder = async (ownerId,petId,date,type,notes) => {
    try {
        const token = localStorage.getItem("token");
        const payload = {
            owner_id: ownerId,
            pet_id: petId,
            date: date,
            type: type,
            notes: notes,
        };
        
        console.log("Sending Reminder: ", JSON.stringify(payload, null, 2));

        const response = await axios.post(`${API_URL}/reminders`, payload, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        console.log("Reminder Added:", response.data);
        return response.data;
    } catch (error) {
        console.error("Add Reminder Error:", error.response?.data || "No Response");
        throw error.response?.data?.error || "Failed to add reminder";
    }
    
};

//Get Reminders
export const getReminders = async (ownerId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_URL}/reminders/${ownerId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        console.log("Reminders Response from API:", response.data);
        return response.data;
    } catch (error) {
        console.error("Get Reminders Error:", error.response?.data || "No Response");
        throw error.response?.data?.error || "Failed to fetch reminders";
    }
};


export const deleteReminder = async (reminderId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.delete(`${API_URL}/reminders/${reminderId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || "Failed to delete reminder";
    }
};