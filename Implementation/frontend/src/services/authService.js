// This Service file is used to make API calls to the Flask API for user authentication

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api"

// Login function for POST request.
export const login = async (email, password) => { 
    try {
      const response = await axios.post(`${API_URL}/login`, { email, password }, { // Send login data in the request body 
          headers: { "Content-Type": "application/json" }, // Proper header for JSON content
          withCredentials: true, 
        });
  
      if (response.data.token && response.data.user_id) { // Check if token and user_id are present in the response
        return response.data; // Return the response data containing token and user_id
      } else {
        throw "Invalid Login Response"; // If the response does not contain token and user_id, throw an error
      }
  
    } catch (error) {
      console.error("Login Error:", error); 
      throw error.response?.data?.error || "Login failed"; 
    }
  };

// Signup function for POST request.
export const signup = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, { email, password }, { // Send signup data in the request body
            headers: {
                "Content-Type": "application/json" }, // Proper header for JSON content
        });
        return response.data;
    } catch (error) {
        console.error("Signup Error:", error);
        throw error.response?.data?.error || "Signup failed";
    }
};

export const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
};

export const sendTestEmail = async () => {
    try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("User not authenticated. Please log in.");

        const response = await axios.post(`${API_URL}/send_test_email`, {}, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || "Failed to send test email";
    }
};