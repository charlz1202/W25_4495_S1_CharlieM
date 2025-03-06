import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export  const sendMessageToChatbot = async (message) => {
    try {
        
        if(!message || typeof message !== 'string') {
            console.error("Invalid message type received", message);
            return {reply: "I don't understand that. Please try again."};
        }
    
        const lowerMessage = message.toLowerCase();

        if(lowerMessage.includes("find") || lowerMessage.includes("search")) {
            const location = "New Westminster, BC";

            const response = await axios.get(`${API_URL}/api/yelp/search`, {
                params: {
                    term: message, location: location
                }
            });

            if(!response.data || !response.data.businesses || response.data.businesses.length === 0) {
                return {reply: "I couldn't find anything for that. Please try again."};
            }

            const businesses = response.data.businesses.map(biz => `${biz.name} - Rating: ${biz.rating} - (${biz.location?.address1 || 'No address available'})`
                
            );

            return {reply: businesses };
        }

        const chatbotResponse = await axios.post(`${API_URL}/api/chatbot`, {message});

        return chatbotResponse.data && chatbotResponse.data.reply ? chatbotResponse.data : {reply: "I don't understand that. Please try again."};

    } catch (error) {
        console.error("Error sending message to chatbot", error);
        return {reply: "I'm sorry, I'm having trouble right now. Please try again later."};
    }
};

         