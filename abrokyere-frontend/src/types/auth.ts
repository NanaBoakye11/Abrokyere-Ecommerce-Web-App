// src/types/auth.ts
import { Customer } from './customer';

export interface LoginResponse {
  token: string;
  customer: Customer;
}
