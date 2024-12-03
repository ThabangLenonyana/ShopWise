import axios from 'axios';

const API_URL = `${process.env.REACT_APP_API_URL}/api`;

// Function to fetch products from the backend
export const fetchProducts = async (searchTerm = '', page = 1) => {
  try {
    const response = await axios.get(`${API_URL}/products/`, {
      params: {
        search: searchTerm,
        page: page,
      },
    });
    return response;
  } catch (error) {
    throw new Error('Failed to fetch products');
  }
};

// Function to search products based on user input
export const searchProducts = async (searchTerm) => {
  try {
    const response = await axios.get(`${API_URL}/products/`, {
      params: {
        search: searchTerm,
      },
    });
    return response;
  } catch (error) {
    throw new Error('Failed to search products');
  }
};

// Function to handle pagination for products
export const paginateProducts = async (page) => {
  try {
    const response = await axios.get(`${API_URL}/products/`, {
      params: {
        page: page,
      },
    });
    return response;
  } catch (error) {
    throw new Error('Failed to paginate products');
  }
};
