import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const sendMessageToChatbot = async (message) => {
    try {
        const response = await axios.post(`${API_URL}/chatbot`, { message,}, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        console.log("Chatbot API Response", response.data);

        return response.data;

    } catch (error) {
        console.error("Chatbot API Error",error.response?.data || error);
        throw error.response?.data?.error || "Failed to send message to chatbot";
        
    }   
};