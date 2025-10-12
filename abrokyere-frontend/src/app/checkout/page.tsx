'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function CheckoutPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleCheckout = async () => {
    setLoading(true);
    try {
      const res = await api.post('/checkout/create-session/');
      window.location.href = res.data.url;  // redirects to Stripe
    } catch (err) {
      console.error('❌ Checkout failed:', err);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto py-10">
      <h1 className="text-2xl font-bold mb-6">Confirm & Pay</h1>
      <p className="text-gray-600 mb-4">Click below to proceed to payment.</p>
      <button
        onClick={handleCheckout}
        disabled={loading}
        className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700"
      >
        {loading ? 'Redirecting...' : 'Proceed to Payment'}
      </button>
    </div>
  );
}
