import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const API_URL = process.env.NODE_ENV === 'production'
  ? 'https://furbot-production.up.railway.app'  // Railway backend URL
  : 'http://127.0.0.1:5000';  // Local backend for development

export default defineConfig({
  plugins: [vue()],
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