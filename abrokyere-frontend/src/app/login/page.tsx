'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import axios from '@/lib/api';
import {LoginResponse} from '@/types/auth'

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);


  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
        const res = await axios.post<LoginResponse>('/auth/login/', { email, password });
        const { token, customer } = res.data;

      // Store token in localStorage (or cookies if you prefer)
      localStorage.setItem('token', token);
      localStorage.setItem('customer', JSON.stringify(customer));
      localStorage.setItem('customer_id', customer.customer_id.toString()); // Also store customer_id directly for convenience


      console.log('🧪 customer email value before saving:', customer.email);
      console.log('🧪 customer stringified First Name:', JSON.stringify(customer.first_name));
      

      localStorage.setItem('loginTimestamp', Date.now().toString()); 
      window.dispatchEvent(new Event('storage-update'));


      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold text-gray-900">Login</h2>
          <p className="text-sm text-gray-500 mt-1">
            Not sure if you have an account? Enter your email and we'll check for you.
          </p>
        </div>
  
        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
  
          <div>
            <label className="text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
  
          {error && <p className="text-red-600 text-sm">{error}</p>}
  
          <button
            type="submit"
            className="w-full py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-900 transition duration-200"
            disabled={loading}
          >
{loading ? (
  <div className="flex items-center justify-center gap-2">
    <svg className="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.37 0 0 5.37 0 12h4z" />
    </svg>
    Signing in...
  </div>
) : 'Continue'}
          </button>
        </form>
  
        <p className="text-xs text-gray-500 mt-4">
          By continuing, you agree to Abrokyere’s{' '}
          <span className="underline cursor-pointer">Terms of Use</span> and{' '}
          <span className="underline cursor-pointer">Privacy Policy</span>.
        </p>
  
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-700">
            New to Abrokyere?{' '}
            <Link href="/register" className="text-black font-semibold hover:underline">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );  
}
