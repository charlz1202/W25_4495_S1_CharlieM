<template>
    <div class="chatbot-icon" @click="toggleChatbot">
        <img src="/chatbot-icon.jpg" alt="Chatbot Icon" class="icon-img" />
    </div>

    <div v-if="showChat" class="chat-container">
        <div class="chat-header">
            <h3>FurBot Chat</h3>
            <button @click="toggleChatbot" class="close-btn">X</button>
        </div>
        <div class="chat-messages">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.from]">
                <p v-if="typeof message.text === 'string'">{{ message.text }}</p>
                
                <!-- Formatting for Yelp Responses -->
                <ul v-else-if="Array.isArray(message.text)" class="business-list">
                    <li v-for="(business, i) in message.text" :key="i" class="business-item">
                        <div class="business-header">
                            🏥 <strong>{{ business.name }}</strong>
                        </div>
                        <div class="business-details">
                            <span v-if="business.rating !== 'N/A'">⭐ <strong>Rating:</strong> {{ business.rating }}</span><br />
                            <span v-if="business.address !== 'No address available'">📍 <strong>Address:</strong> {{ business.address }}</span>
                        </div>
                    </li>
                </ul>

                <p v-else>{{ message.text || "I couldn't understand that." }}</p>
            </div>
        </div>
    <div class="chat-input">
        <input v-model="newMessage" placeholder="Ask FurBot...." @keyup.enter="sendMessage" />
        <button @click="sendMessage" class="send-btn">Send</button>
    </div>
</div>
</template>

<script>
import { sendMessageToChatbot } from "../services/chatService.js";

export default {
    data() {
        return {
            showChat: false,
            messages: [{text: "Hi! How can I help you today?", from: "bot"}],
            newMessage: "",
        };
    },
    methods: {
        toggleChatbot() {
            this.showChat = !this.showChat;
        },
        async sendMessage() {
            if (!this.newMessage.trim()) return;

            if(!Array.isArray(this.messages)) {
                this.messages = [];
            } 

            this.messages.push({ text: this.newMessage, from: "user" });

            try {

                console.log("Sending message to chatbot: ", this.newMessage);
                const response = await sendMessageToChatbot(this.newMessage);

                console.log("Chatbot response: ", response);

                if(!response|| typeof response !== "object" || !("reply" in response)) {
                    this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
                    return;
                }

                if(Array.isArray(response.reply)) {
                  const formattedBusinesses = response.reply.map((business) => {
                    return {
                      name: business.name || "No name available",
                      rating: business.rating || "N/A",
                      address: business.address || "No address available"
                    };
                  });
                  
                    this.messages.push({ text: formattedBusinesses, from: "bot" });
                } else {
                    this.messages.push({ text: response.reply || "Sorry, I didn't understand that.", from: "bot" });
                }
            } catch (error) {
                console.error("Error sending message to chatbot: ", error);
                this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
            }

            this.newMessage = "";          
        },
    },
};

</script>


<style scoped>

/* Business List Styling */
.business-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

/* Individual Business Item */
.business-item {
  background: #f9f9f9;
  padding: 10px;
  margin: 8px 0;
  border-radius: 8px;
  border-left: 5px solid #ff9800; /* Orange highlight */
  font-size: 13px;
  display: flex;
  flex-direction: column;
}

/* Header Styling for Business Name */
.business-header {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Business Details Styling */
.business-details {
  font-size: 12px;
  color: #555;
  margin-top: 5px;
  line-height: 1.4;
}

/* Message Style */
.message {
  padding: 10px;
  margin: 6px 0;
  border-radius: 5px;
  font-size: 12px;
}

/* User Message */
.user {
  background: #007bff;
  color: white;
  align-self: flex-end;
}

/* Bot Message */
.bot {
  background: #f0f0f0;
  color: #333;
  align-self: flex-start;
}


/* Floating Chatbot Icon */
.chatbot-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #ff9800;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.icon-img {
  width: 30px;
  height: 30px;
}

/* Chat Container */
.chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #fff;
  width: 300px;
  height: 400px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

/* Chat Header */
.chat-header {
  background: #ff9800;
  color: #fff;
  padding: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

/* Chat message style */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  font-size: 12px;
}

/* Chat input from user */
.chat-input {
  display: flex;
  gap: 10px;
  padding: 10px;
}   

.chat-input button {
  padding: 8px 12px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input button:hover {
  background: #0056b3;
}


</style>