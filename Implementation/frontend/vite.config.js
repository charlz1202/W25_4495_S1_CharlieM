import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173, // Your frontend will run on this port
    proxy: {
      '/api': { 
        target: 'http://localhost:5000', // Your Flask backend
        changeOrigin: true,
        secure: false, // Use this if calling an HTTPS backend
        rewrite: (path) => path.replace(/^\/api/, ''), // Removes '/api' prefix before sending the request
      }
    }
  },
})