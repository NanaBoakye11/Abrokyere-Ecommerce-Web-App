// lib/api.ts
import axios from 'axios';
import { Product } from '../types/product';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
console.log("💥 API base URL:", API_BASE_URL);


const api = axios.create({
  baseURL: `${API_BASE_URL}/api`, // Django API
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});


api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    config.headers = config.headers ?? {};
    
    if (token) {
      (config.headers as any).Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // Check if it's a 401 response and not a login request itself, and not already retried
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/auth/login/') {
      originalRequest._retry = true;
      // In a real app, you'd try to refresh the token here using the refresh token.
      // For now, we'll just clear the session and redirect to login.
      console.warn("🛑 JWT expired or invalid. User will be logged out.");
      console.warn("Authentication failed or token expired. Clearing session.");
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken'); 
      localStorage.removeItem('customer');
      localStorage.removeItem('customer_id');
      window.dispatchEvent(new Event('storage-update')); // Notify other components that auth state changed
      // Redirect to login page if not already there
      if (window.location.pathname !== '/login') {
          window.location.href = '/login'; 
      }
      return Promise.reject(error); // Reject the original request
    }
    return Promise.reject(error); // For other errors, just re-throw
  }
);

export default api;

export const fetchFeaturedProducts = () => api.get<Product[]>(`/products/featured/`);
export const fetchProductsByCategory = (categoryId: number) => api.get(`/products/category/${categoryId}/`);
export const fetchGroupedProducts = async () => {
  return api.get(`/products/grouped/`);
};
export async function fetchProductById(productId: string) {
  return api.get(`/products/${productId}/`);
}

export const addToCart = async (data: {
  product_id: string;
  quantity: number;
}) => {
  return api.post('/cart/add/', data); // global token handled in interceptor
};





// export const addToCart = (data: {
//   // customer_id: string;
//   product_id: string;
//   quantity: number;
// }) => api.post('/cart/add/', data);


// export const addToCart = async (data: {
//   product_id: string;
//   quantity: number;
// }) => {
//   const token = localStorage.getItem('token'); // retrieve JWT token

//   return api.post('/cart/add/', data, {
//     headers: {
//       Authorization: `Bearer ${token}`,
//     },
//   });
// };

// api.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem('token'); // Get token from localStorage (make sure 'authToken' is the key you use)
    
//     config.headers = config.headers || {};

//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`; // Add Bearer token to headers
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );