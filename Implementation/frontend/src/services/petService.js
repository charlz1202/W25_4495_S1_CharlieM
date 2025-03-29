import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";


export const getPets = async (ownerId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${API_URL}/pets/${ownerId}`, {
            headers: {Authorization: `Bearer ${token}`},
        });

        console.log("Pets Response from Flask:", response.data);

        return response.data;
    } catch (error) {
        console.error("Get Pets Error:", error);
        throw error.response?.data?.error || "Failed to fetch pets";
    }
};

export const addPet = async (ownerId, petName, species, dob, color, breed  ) => {
    try {
        const token = localStorage.getItem("token");

        if(!ownerId) {
            throw new Error("Owner ID is required to add a pet");
        }

        const payload = {
            owner_id: String(ownerId),
            name: petName,
            species: species || "",
            dob: dob,
            color: color || "",
            breed: breed || "",
        };

        console.log("Sending payload to Flask:", JSON.stringify(payload, null, 2)); // Debugging step

        const response = await axios.post(`${API_URL}/pets`, payload, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        return response.data;
    } catch (error) {
        console.error("Add Pet Error:", error);
        console.error("Full Error Response:", error.response ? error.response.data : "No Response");

        throw error.response?.data?.error || "Failed to add pet";
    }   

};

export const deletePet = async (petId) => {
    try {
        const token = localStorage.getItem("token");
        const response = await axios.delete(`${API_URL}/pets/${petId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error("Delete Pet Error:", error);
        throw error.response?.data?.error || "Failed to delete pet";
    }
};
