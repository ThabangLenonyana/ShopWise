import axios from 'axios';

const API_URL = `${process.env.REACT_APP_API_URL}/api`;

// Function to fetch categories from the backend
export const fetchCategories = async () => {
  try {
    const response = await axios.get(`${API_URL}/categories/`);
    return response;
  } catch (error) {
    throw new Error('Failed to fetch categories');
  }
};

// Function to fetch retailers from the backend
export const fetchRetailers = async () => {
  try {
    const response = await axios.get(`${API_URL}/retailers/`);
    return response;
  } catch (error) {
    throw new Error('Failed to fetch retailers');
  }
};

// Function to fetch products from the backend
export const fetchProducts = async (searchTerm = '', page = 1, filters = {}, page_size = 24) => {
  try {
    const response = await axios.get(`${API_URL}/products/`, {
      params: {
        search: searchTerm,
        page: page,
        page_size: page_size,
        category: filters.category,
        retailer: filters.retailer,
      },
    });
    return {
      data: response.data.results,
      pagination: {
        currentPage: response.data.current_page,
        totalPages: response.data.total_pages,
        count: response.data.count
      }
    };
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
