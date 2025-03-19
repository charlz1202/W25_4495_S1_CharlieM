import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const isProduction = process.env.NODE_ENV === 'production';

const API_URL = isProduction
  ? "https://furbot-production.up.railway.app"  // Production backend
  : "http://127.0.0.1:5000";  // Local backend

export default defineConfig({
  plugins: [vue()],
  base: "/",  // Ensures correct routing in production
  server: {
    port: 5173, // local frontend will run on this port
    proxy: {
      '/api': { 
        target: API_URL, // Flask backend
        changeOrigin: true, // Virtual hosted sites
        rewrite: (path) => path.replace(/^\/api/, ""),
      }
    }
  },
  define: {
    __API_URL__: JSON.stringify(API_URL), // Makes API_URL available globally
  },
});