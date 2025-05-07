// lib/api.ts
import axios from 'axios';
import { Product } from '../types/product';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Django API
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
export const fetchFeaturedProducts = () => api.get<Product[]>('/products/featured/');
export const fetchProductsByCategory = (categoryId: number) => api.get(`/products/category/${categoryId}/`);

