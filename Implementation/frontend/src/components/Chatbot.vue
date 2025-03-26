<template>
  <!-- Always-visible embedded chatbot -->
  <div class="chat-container chatbot-embedded">
    <div class="chat-header">
      <h3>FurBot Chat</h3>
    </div>

    <div class="chat-messages">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.from]">
        <p v-if="typeof message.text === 'string'">{{ message.text }}</p>

        <!-- Yelp Business List Format -->
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

    <!-- Input Area -->
    <div class="chat-input">
      <input v-model="newMessage" placeholder="Ask FurBot..." @keyup.enter="sendMessage" />
      <button @click="sendMessage" class="send-btn">Send</button>
    </div>
  </div>
</template>

<script>
import { sendMessageToChatbot } from "../services/chatService.js";

export default {
  data() {
    return {
      messages: [{ text: "Hi! How can I help you today?", from: "bot" }],
      newMessage: "",
    };
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim()) return;

      this.messages.push({ text: this.newMessage, from: "user" });

      try {
        const response = await sendMessageToChatbot(this.newMessage);

        if (!response || typeof response !== "object" || !("reply" in response)) {
          this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
          return;
        }

        if (Array.isArray(response.reply)) {
          const formatted = response.reply.map((business) => ({
            name: business.name || "No name available",
            rating: business.rating || "N/A",
            address: business.address || "No address available",
          }));
          this.messages.push({ text: formatted, from: "bot" });
        } else {
          this.messages.push({ text: response.reply || "Sorry, I didn't understand that.", from: "bot" });
        }
      } catch (error) {
        console.error("Error sending message to chatbot:", error);
        this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
      }

      this.newMessage = "";
    },
  },
};
</script>

<style scoped>
.chat-container {
  background: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chatbot-embedded {
  width: 100%;
  max-width: 380px;
  height: 850px;        
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-header {
  background: #ff9800;
  color: #fff;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  font-size: 12px;
}

.message {
  padding: 10px;
  margin: 6px 0;
  border-radius: 5px;
}

.user {
  background: #007bff;
  color: white;
  align-self: flex-end;
}

.bot {
  background: #f0f0f0;
  color: #333;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
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

.business-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center; 
}

.business-item {
  background: #f9f9f9;
  padding: 10px;
  margin: 8px 0;
  border-radius: 8px;
  border-left: 5px solid #ff9800;
  font-size: 13px;
  display: flex;
  flex-direction: column;
  width: 90%; 
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.business-header {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 5px;
}

.business-details {
  font-size: 12px;
  color: #555;
  margin-top: 5px;
  line-height: 1.4;
}
</style>