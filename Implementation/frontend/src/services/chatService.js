import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export  const sendMessageToChatbot = async (message) => {
    try {
        
        if(!message || typeof message !== 'string') {
            console.error("Invalid message type received", message);
            return {reply: "I don't understand that. Please try again."};
        }
    
        const lowerMessage = message.toLowerCase();

        // Pet Service Detection
        if(lowerMessage.includes("find") || lowerMessage.includes("search") || lowerMessage.includes("nearest")) {
            let searchTerm="";
            let category = "";

            // Detect Service Type

            if(lowerMessage.includes("groomer") || lowerMessage.includes("grooming")) {
                searchTerm = "pet groomers";
                category = "groomer";
            }
            else if(lowerMessage.includes("vet") || lowerMessage.includes("veterinarian")) {
                searchTerm = "veterinarians";
                category = "vet";
            }
            else if(lowerMessage.includes("pet store") || lowerMessage.includes("shop")) {
                searchTerm = "pet store";
                category = "petstore";
            }
            else if(lowerMessage.includes("dog park") || lowerMessage.includes("park")) {
                searchTerm = "dog park";
                category = "dog_parks";
            }
            else if(lowerMessage.includes("daycare") || lowerMessage.includes("boarding")) {
                searchTerm = "pet daycare";
                category = "petboarding";
            }
            else if(lowerMessage.includes("trainer") || lowerMessage.includes("training")) {
                searchTerm = "dog training";
                category = "pet_training";
            }
            else {
                searchTerm = "pet services";
                category = "petservices,groomer,vet,dog_parks,petstore";
            }

            const location = "New Westminster, BC";

            // Call Yelp API for Pet Services
            const response = await axios.get(`${API_URL}/api/yelp/search`, {
                params:{term: searchTerm, location: location, categories: category}
            });

            if(!response.data || !response.data.businesses || response.data.businesses.length === 0) {
                return{reply: `I couldn't find any ${searchTerm} near you. Try a different location!`};
            }

            // Format Pet Service Results
            const services = response.data.businesses.map(service => ({
                name: service.name,
                rating: service.rating || "N/A",
                address: service.location?.address1 || "No address available"
            }));

            return {reply: services};
        }

        // Default Chatbot Response
        const chatbotResponse = await axios.post(`${API_URL}/api/chatbot`, {message});
        
        return chatbotResponse.data && chatbotResponse.data.reply
            ? chatbotResponse.data
            : {reply: "I don't understand that. Please try again."};

    } catch(error) {
        console.error("Error sending message to chatbot:", error);
        return { reply:"I'm sorry, I'm having trouble right now. Please try again later."};
    }
};

        
        
        
        

         