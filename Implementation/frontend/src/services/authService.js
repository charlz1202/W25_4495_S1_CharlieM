// This Service file is used to make API calls to the Flask API for user authentication

import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000'; // Flask API

// Login function for POST request.
export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password });

    if (response.data.token && response.data.user_id) {
        return response.data;
    } else {
      throw "Invalid Login Response";
    }

    
  } catch (error) {
    throw error.response?.data?.error || "Login failed";
  }
};

// Signup function for POST request.
export const signup = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, { email, password });
        return response.data;  
    } catch (error) {
        throw error.response?.data?.error || "Signup failed";
    }
};

export const logout = () => {
    localStorage.removeItem("token");
};

export const sendTestEmail = async () => {
    try {
        const token = localStorage.getItem("token");
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