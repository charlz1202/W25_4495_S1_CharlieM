import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export const sendMessageToChatbot = async (message) => {
    try {
        
        if(!message || typeof message !== 'string') {
            console.error("Invalid message type received", message);
            return {reply: "I don't understand that. Please try again."};
        }
    
        const lowerMessage = message.toLowerCase();

        console.log("Message received:", lowerMessage);

        // Pet Service Detection
        if(
            lowerMessage.includes("find") ||
            lowerMessage.includes("search") ||
            lowerMessage.includes("nearest") ||
            lowerMessage.includes("near") ||
            lowerMessage.includes("nearby") ||
            lowerMessage.includes("near me")
          ) {
            let searchTerm="";
            let category = "";
            let attributes = ""; // Optional attributes for Yelp API for dog-friendly places keyword

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
            else if(lowerMessage.includes("restaurant") || lowerMessage.includes("cafe") || lowerMessage.includes("eat")) {
                searchTerm = "restaurants";
                category = "restaurants";
                attributes = "dog_friendly";
            }
            else if(lowerMessage.includes("hotel") || lowerMessage.includes("stay") || lowerMessage.includes("accommodation")) {
                searchTerm = "hotels";
                category = "hotels";
                attributes = "dog_friendly";
            }
            else {
                searchTerm = "pet services";
                category = "petservices,groomer,vet,dog_parks,petstore";
            }

            const location = "Vancouver, BC"; // Default location

            // Call Yelp API for Pet Services
            const response = await axios.get(`${API_URL}/yelp/search`, {
                params:{term: searchTerm, location: location, category: category}
            });

            console.log("Yelp full response:", response.data); 

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
        const chatbotResponse = await axios.post(`${API_URL}/chatbot`, {message});
        
        return chatbotResponse.data && chatbotResponse.data.reply
            ? chatbotResponse.data
            : {reply: "I don't understand that. Please try again."};

    } catch(error) {
        console.error("Error sending message to chatbot:", error);
        return { reply:"I'm sorry, I'm having trouble right now. Please try again later."};
    }
};