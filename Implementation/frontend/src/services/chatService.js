import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const sendMessageToChatbot = async (message) => {
    try {
        
        if (message.toLowerCase().includes("find") || message.toLowerCase().includes("search")) {
            const location = "New Westminster, BC";
            const response = await axios.get(`/api/yelp/search`, {
                params: {
                    term:message,
                    location: location
                }
        });

        const businesses = response.data.businesses.map(biz => 
            '${biz.name} - Rating: ${biz.rating} - ${biz.location.address1}'
        ).join("\n");

        return {
            reply: businesses || "No results found"};
        }

        const chatbotResponse = await axios.post("/api/chatbot", {
            message
        });
        return chatbotResponse.data;

    } catch (error) {
        console.error(error);
        return { reply: "Sorry, something went wrong" };
    }
};