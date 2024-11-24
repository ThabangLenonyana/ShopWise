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

export const register = async (email, username, password, password2,) => {
  try {
    const response = await axios.post(`${API_URL}/register/`, {
      email,
      username,
      password,
      password2,
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

export const verifyEmail = async (token) => {
  try {
    const response = await axios.post(`${API_URL}/verify-email/`, { token }, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response;
  } catch (error) {
    throw handleApiError(error);
  }
};

export const fetchUserProfile = async () => {

  const token = localStorage.getItem('token');
    console.log('Token being sent:', token);

    if (!token) {
      throw new Error('User is not logged in');
    }
    
  try {

    const response = await axios.get(`${API_URL}/profile/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });
    return response;
  } catch (error) {
    throw handleApiError(error);
  }
};

export const updateUserProfile = async (profileData) => {
  try {
    const response = await axios.put(`${API_URL}/profile/`, profileData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      
      }
    });
    return response;
  } catch (error) {
    throw handleApiError(error);
  }
}