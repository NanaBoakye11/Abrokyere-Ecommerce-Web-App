'use client';

import { useRouter } from 'next/navigation';

export default function OrderErrorPage() {
  const router = useRouter();
  return (
    <div className="max-w-xl mx-auto px-6 py-16 text-center">
      <h1 className="text-3xl font-bold mb-3">Payment canceled</h1>
      <p className="text-gray-600">
        Your payment was not completed. You can try again or keep shopping.
      </p>
      <div className="mt-8 flex gap-3 justify-center">
        <button onClick={() => router.push('/cart')} className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
          Return to Cart
        </button>
        <button onClick={() => router.push('/')} className="px-4 py-2 rounded border hover:bg-gray-50">
          Continue Shopping
        </button>
      </div>
    </div>
  );
}
