'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setSuccess('');

      const res = await api.post<{ message: string }>('/auth/register/', {
        first_name: form.first_name,
        last_name: form.last_name,
        email: form.email,
        phone: form.phone,
        password: form.password,
      });

      setSuccess(res.data.message);
      setForm({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
      });

      setTimeout(() => {
        router.push('/login');
      }, 1000);
    } catch (err: any) {
      setError(err?.response?.data?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold text-gray-900">Create your account</h2>
          <p className="text-sm text-gray-500">Join the Abrokyere experience 🌍</p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          {error && <p className="text-red-600 text-sm">{error}</p>}
          {success && <p className="text-green-600 text-sm">{success}</p>}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">First Name</label>
              <input
                type="text"
                name="first_name"
                value={form.first_name}
                onChange={handleChange}
                required
                className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Last Name</label>
              <input
                type="text"
                name="last_name"
                value={form.last_name}
                onChange={handleChange}
                required
                className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700">Phone</label>
            <input
              type="tel"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              required
              className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                required
                className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={form.confirmPassword}
                onChange={handleChange}
                required
                className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg bg-white text-black placeholder-gray-400 focus:ring-2 focus:ring-black focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-900 transition duration-200 disabled:opacity-50"
          >
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500">
          Already registered?{' '}
          <a href="/login" className="text-black font-semibold hover:underline">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}






































