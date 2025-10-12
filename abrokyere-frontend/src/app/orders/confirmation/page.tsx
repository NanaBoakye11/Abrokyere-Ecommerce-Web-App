'use client';

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import api from '@/lib/api';

interface OrderItem {
  order_item_id: number;
  product_name: string;
  quantity: number;
  price: number;
}

interface Order {
  order_id: number;
  order_date: string;
  total_amount: number;
  status: string;
  items: OrderItem[];
}

export default function OrderConfirmationPage() {
  const params = useSearchParams();
  const router = useRouter();
  const sessionId = params.get('session_id');
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);

  const tryLoadOrder = useMemo(() => {
    return async () => {
      try {
        if (sessionId) {
          // primary: lookup via session id
          const { data } = await api.get(`/orders/by-session/${sessionId}/`);
          setOrder(data);
          setLoading(false);
          return true;
        }
      } catch {
        // noop, will fallback
      }
      try {
        // fallback: recent orders (take the first)
        const { data } = await api.get('/orders/recent/');
        const first = data?.orders?.[0];
        if (first) setOrder(first);
      } catch (e) {
        // ignore
      } finally {
        setLoading(false);
      }
      return false;
    };
  }, [sessionId]);

  useEffect(() => {
    let cancelled = false;

    const poll = async () => {
      // Poll up to ~10s for the webhook to finish
      const start = Date.now();
      while (!cancelled && Date.now() - start < 10_000) {
        const found = await tryLoadOrder();
        if (found) return;
        await new Promise(r => setTimeout(r, 1200));
      }
      if (!cancelled) await tryLoadOrder(); // final attempt + fallback
    };

    poll();
    return () => {
      cancelled = true;
    };
  }, [tryLoadOrder]);

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-16 text-center">
        <h1 className="text-2xl font-semibold">Finalizing your order…</h1>
        <p className="text-gray-500 mt-2">We’re confirming your payment.</p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-16 text-center">
        <h1 className="text-2xl font-semibold mb-2">Thanks for your purchase!</h1>
        <p className="text-gray-600">
          We couldn’t find the order yet. It might take a moment to appear.
        </p>
        <div className="mt-8 flex gap-3 justify-center">
          <button onClick={() => router.push('/orders')} className="px-4 py-2 rounded bg-gray-900 text-white hover:bg-black">
            View Orders
          </button>
          <button onClick={() => router.push('/')} className="px-4 py-2 rounded border hover:bg-gray-50">
            Continue Shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-bold">Order Confirmed 🎉</h1>
      <p className="text-gray-600 mt-2">Order #{order.order_id}</p>

      <div className="mt-8 border rounded-lg p-6 bg-white">
        <h2 className="text-lg font-semibold mb-4">Items</h2>
        <div className="space-y-3">
          {order.items.map((it) => (
            <div key={it.order_item_id} className="flex justify-between text-sm border-b pb-2">
              <div>
                <p className="font-medium">{it.product_name}</p>
                <p className="text-gray-500">Qty {it.quantity}</p>
              </div>
              <p>${Number(it.price).toFixed(2)}</p>
            </div>
          ))}
        </div>

        <div className="flex justify-between mt-6 pt-4 border-t text-lg font-semibold">
          <span>Total</span>
          <span>${Number(order.total_amount).toFixed(2)}</span>
        </div>
      </div>

      <div className="mt-8 flex gap-3">
        <button onClick={() => router.push('/orders')} className="px-4 py-2 rounded bg-gray-900 text-white hover:bg-black">
          See All Orders
        </button>
        <button onClick={() => router.push('/')} className="px-4 py-2 rounded border hover:bg-gray-50">
          Continue Shopping
        </button>
      </div>
    </div>
  );
}







// 'use client';

// import { useSearchParams, useRouter } from 'next/navigation';
// import { useEffect } from 'react';

// export default function OrderConfirmationPage() {
//   const params = useSearchParams();
//   const router = useRouter();
//   const sessionId = params.get('session_id');

//   useEffect(() => {
//     // IMPORTANT: The webhook is the source of truth.
//     // We don’t create orders here. But you COULD poll a /orders/by-session/{id}/ endpoint
//     // if you later add it, to display order details after your webhook finishes.
//   }, [sessionId]);

//   return (
//     <div className="max-w-2xl mx-auto px-6 py-16 text-center">
//       <h1 className="text-3xl font-bold mb-3">Thanks for your purchase! 🎉</h1>
//       <p className="text-gray-600">
//         Your payment was successful. We’re preparing your order.
//       </p>
//       {sessionId && (
//         <p className="text-xs text-gray-400 mt-2">
//           Checkout Session ID: <code>{sessionId}</code>
//         </p>
//       )}
//       <div className="mt-8 flex gap-3 justify-center">
//         <button
//           onClick={() => router.push('/orders')}
//           className="px-4 py-2 rounded bg-gray-900 text-white hover:bg-black"
//         >
//           View Orders
//         </button>
//         <button
//           onClick={() => router.push('/')}
//           className="px-4 py-2 rounded border hover:bg-gray-50"
//         >
//           Continue Shopping
//         </button>
//       </div>
//     </div>
//   );
// }






