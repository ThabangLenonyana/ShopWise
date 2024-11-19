import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/auth';

// Add error handling wrapper
const handleApiError = (error) => {
  if (!navigator.onLine) {
    throw new Error('Please check your internet connection');
  }
  
  if (error.response?.data) {
    throw new Error(error.response.data.detail || error.response.data.message || error.response.data.error);
  }
  
  throw new Error('An unexpected error occurred. Please try again later.');
};

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, {
      email,
      password
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response;
  } catch (error) {
    throw handleApiError(error);
  }
};

export const register = async (username, email, password, password2, firstName, lastName) => {
  try {
    const response = await axios.post(`${API_URL}/register/`, {
      username,
      email,
      password,
      password2,
      first_name: firstName, 
      last_name: lastName
    }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response;
  } catch (error) {
    throw handleApiError(error);
  }
};