<template>
  <div>
    <div v-if="loading">Favorite List</div>
    <div v-else-if="favorites.length === 0">You have no favorites saved yet.</div>
    <ul v-else class="favorites-list">
      <li v-for="fav in favorites" :key="fav._id" class="favorite-item">
        <div class="fav-info">
          <strong>{{ fav.name }}</strong><br />
          😊 {{ fav.rating }}<br />
          📍 {{ fav.location }}
        </div>
        <button @click="removeFavorite(fav._id)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      favorites: [],
      loading: true,
    };
  },
  methods: {
    async fetchFavorites() {
      const userId = localStorage.getItem("user_id");
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/favorites/${userId}`);
        const data = await res.json();
        this.favorites = data;
      } catch (err) {
        console.error("Failed to load favorites", err);
      } finally {
        this.loading = false;
      }
    },
    async removeFavorite(favId) {
      try {
        await fetch(`${import.meta.env.VITE_API_URL}/api/favorites/${favId}`, {
          method: "DELETE",
      }); 
        this.favorites = this.favorites.filter((f) => f._id !== favId);
      } catch (err) {
        console.error("Failed to remove favorite", err);
      }
    },
  },
  mounted() {
    this.fetchFavorites();
  },
};
</script>

<style scoped>
.favorites-list {
  padding: 0;
  margin: 0;
  list-style-type: none;
}
.favorite-item {
  background: #797878;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgb(255, 255, 255);
}
.fav-info {
  font-size: 14px;
  line-height: 1.5;
}
button {
  background: #ef5350;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background: #d32f2f;
}
</style>