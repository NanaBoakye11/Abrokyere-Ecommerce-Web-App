// lib/api.ts
import axios from 'axios';
import { Product } from '../types/product';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`, // Django API
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;

export const fetchFeaturedProducts = () => api.get<Product[]>(`/products/featured/`);
export const fetchProductsByCategory = (categoryId: number) => api.get(`/products/category/${categoryId}/`);
export const fetchGroupedProducts = async () => {
  return api.get(`/products/grouped/`);
};
export async function fetchProductById(productId: string) {
  return api.get(`/products/${productId}/`);
}

export const addToCart = (data: {
  product_id: string;
  quantity: number;
}) => api.post('/cart/add/', data);

