<template>
  <!-- Always-visible embedded chatbot -->
  <div class="chat-container chatbot-embedded">
    <div class="chat-header">
      <h3>FurBot Chat</h3>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.from, { 'loading-msg': message.loading }]"
      >
      
      <p v-if="typeof message.text === 'string'" v-html="message.text"></p>

        <!-- Yelp Business List Format -->
        <ul
          v-else-if="Array.isArray(message.text)"
          class="business-list"
        >
          <li
            v-for="(business, i) in message.text"
            :key="i"
            class="business-item"
          >
            <div class="business-header">
              {{ categoryIcon(business.name) }} <strong>{{ business.name }}</strong>
            </div>
            <div class="business-details">
              <span v-if="business.rating !== 'N/A'">
               😊  <strong>Rating:</strong> {{ business.rating }}
              </span>
              <br />
              <span v-if="business.address !== 'No address available'">
                📌 <strong>Address:</strong> {{ business.address }}
              </span>
            </div>
               
           <button @click="saveToFavorites(business)" class="fav-btn">
            ⭐ Add to Favorites
          </button>
         </li>
        </ul>

        <p v-else>{{ message.text || "I couldn't understand that." }}</p>
      </div>
    </div>

    <!-- Input Area -->
    <div class="chat-input">
      <input
        v-model="newMessage"
        placeholder="Ask FurBot..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage" class="send-btn">Send</button>
    </div>
  </div>
</template>

<script>
import { sendMessageToChatbot } from "../services/chatService.js";

export default {
  data() {
    return {
      messages: [{
        text: "🐩 Hi! I'm FurBot — I can help with pet travel, finding vets & groomers.\n\nTry asking:\n• How to bring my dog to Canada?\n• What airlines allow dogs?\n• Find groomers near me",
        from: "bot"
  }],
      newMessage: "",
    };
  },
  methods: 
  {
    async sendMessage() {
      if (!this.newMessage.trim()) return;

      const userText = this.newMessage;
      this.messages.push({ text: userText, from: "user" });
      this.$nextTick(() => this.scrollToBottom());

      // Add "typing..." message while waiting for response
      const typingMsg = { text: "FurBot is typing...", from: "bot", loading: true };
      this.messages.push(typingMsg);
      this.$nextTick(() => this.scrollToBottom());

      try {
        const response = await sendMessageToChatbot(userText);

        // Remove "typing..." before adding real reply
        this.messages = this.messages.filter(msg => !msg.loading);

        if (!response || typeof response !== "object" || !("reply" in response)) {
          this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
          this.$nextTick(() => this.scrollToBottom());
          return;
        }

        if (Array.isArray(response.reply)) {
          const formatted = response.reply.map((business) => ({
            name: business.name || "No name available",
            rating: business.rating || "N/A",
            address: business.address || "No address available",
            image_url: business.image_url || "",                  
            business_id: business.id || business.name             
          }));
          this.messages.push({ text: formatted, from: "bot" });
        } else {
          this.messages.push({
            text: response.reply || "Sorry, I didn't understand that.",
            from: "bot",
          });
        }
        this.$nextTick(() => this.scrollToBottom());
      } catch (error) {
        console.error("Error sending message to chatbot:", error);
        this.messages = this.messages.filter(msg => !msg.loading);
        this.messages.push({ text: "Sorry, I didn't understand that.", from: "bot" });
        this.$nextTick(() => this.scrollToBottom());
      }

      this.newMessage = "";
    },

    scrollToBottom() {
      this.$nextTick(() => 
      {
        const container = this.$refs.messagesContainer;
        if (container) 
        {
          container.scrollTop = container.scrollHeight + 1000;
        }
      });
    },

    categoryIcon(name) {
      const lowerName = name.toLowerCase();
      if (lowerName.includes("hotel")) return "🏨";
      if (lowerName.includes("restaurant") || lowerName.includes("cafe")) return "🍽️";
      if (lowerName.includes("groom") || lowerName.includes("salon")) return "✂️";
      if (lowerName.includes("vet") || lowerName.includes("clinic")) return "🐾";
      if (lowerName.includes("park")) return "🏞️";
      return "🏠"; // default icon
   },

   // Function to save a business to favorites
    async saveToFavorites(business) {
    const ownerId = localStorage.getItem("user_id");
    if (!ownerId) {
      alert("You need to be logged in to save favorites.");
      return;
    }

    const payload = {
      owner_id: ownerId,
      business_id: business.business_id || business.name,
      name: business.name || "Unnamed",
      image_url: business.image_url || "",
      rating: business.rating || "N/A",
      location: business.address || "Unknown location",
    };

      try {
        // Send a POST request to save the favorite
        const response = await fetch("/api/favorites", {
          method: "POST",
          headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      
        if (response.ok) {
          alert("✅Added to Favorites!");
          this.$emit("favorite-added"); // Emit event to refresh favorite list in Dashboard.vue
        } else {
          alert(result.error || "Something went wrong.");
        }
    } catch (err) {
      console.error("Failed to save favorite:", err);
      alert("Failed to save favorite.");
    } 
  },
},


};
</script>

<style scoped>
.fav-btn {
  margin-top: 8px;
  background: #ff9800;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}
.fav-btn:hover {
  background: #e68900;
}
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
  height: 600px;
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  font-size: 13px;
  max-height: 100%;
}

.message {
  padding: 10px;
  margin: 6px 0;
  border-radius: 5px;
  word-wrap: break-word;
  white-space: pre-wrap;
  max-width: 100%;
  overflow-wrap: break-word;
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

.loading-msg {
  font-style: italic;
  color: #777;
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