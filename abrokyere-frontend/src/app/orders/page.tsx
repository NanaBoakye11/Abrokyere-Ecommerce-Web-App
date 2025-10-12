// export default function OrdersTest() {
//   return (
//     <main className="p-6">
//       <h1 className="text-2xl font-bold">Orders route is working ✅</h1>
//       <p className="mt-2 text-gray-600">If you can see this, /orders is registered.</p>
//     </main>
//   );
// }




'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import Link from 'next/link';

interface OrderItem {
  order_item_id: number;
  product_id: number;
  product_name?: string | null;
  quantity: number;
  price: number; // unit price
}

interface Order {
  order_id: number;
  order_date: string | null;
  status: string | null;
  total_amount: number;
  items: OrderItem[];
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get('/orders/recent/');
        setOrders(res.data?.orders ?? []);
      } catch (e) {
        console.error('Failed to load orders:', e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div className="max-w-5xl mx-auto p-6">Loading orders…</div>;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Orders</h1>

      {orders.length === 0 ? (
        <div className="rounded border p-6 bg-white">
          <p className="text-gray-600">You don’t have any orders yet.</p>
          <Link href="/" className="inline-block mt-4 text-indigo-600 hover:underline">
            Continue shopping →
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((o) => (
            <div key={o.order_id} className="rounded border bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold">Order #{o.order_id}</p>
                  <p className="text-sm text-gray-500">
                    {o.order_date ? new Date(o.order_date).toLocaleString() : '—'}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold">${o.total_amount.toFixed(2)}</p>
                  <p className="text-sm text-gray-500">{o.status ?? '—'}</p>
                </div>
              </div>

              <div className="mt-4 divide-y">
                {o.items.map((it) => (
                  <div key={it.order_item_id} className="py-3 flex items-center justify-between">
                    <div>
                      <p className="font-medium">{it.product_name ?? `Product #${it.product_id}`}</p>
                      <p className="text-sm text-gray-600">Qty: {it.quantity}</p>
                    </div>
                    <div className="text-sm text-gray-700">
                      ${(it.price * it.quantity).toFixed(2)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}












// 'use client';

// import { useEffect, useState } from 'react';
// import api from '@/lib/api';
// import Link from 'next/link';

// type OrderItem = {
//   order_item_id: number;
//   product_id: number;
//   product_name?: string | null;
//   quantity: number;
//   price: number; // unit price
// };

// type Order = {
//   order_id: number;
//   order_date: string | null;
//   status: string | null;
//   total_amount: number;
//   items: OrderItem[];
// };

// export default function OrdersPage() {
//   const [orders, setOrders] = useState<Order[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [err, setErr] = useState<string | null>(null);

//   const fetchOrders = async () => {
//     try {
//       setLoading(true);
//       setErr(null);
//       const res = await api.get<{ orders: Order[] }>('/orders/recent/');
//       setOrders(res.data.orders || []);
//     } catch (e: any) {
//       console.error('Failed to load orders', e);
//       setErr('Could not load your recent orders.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     // require auth token in localStorage (your axios interceptor will attach it)
//     const token = localStorage.getItem('token');
//     const ts = localStorage.getItem('loginTimestamp');
//     const twoDays = 2 * 24 * 60 * 60 * 1000;

//     if (!token || !ts || Date.now() - parseInt(ts) > twoDays) {
//       // optional: redirect to login
//       // window.location.href = '/login';
//       setLoading(false);
//       setErr('Please sign in to view your orders.');
//       return;
//     }

//     fetchOrders();
//   }, []);

//   if (loading) {
//     return (
//       <div className="max-w-5xl mx-auto p-6">
//         <h1 className="text-2xl font-bold mb-4">Your Orders</h1>
//         <p className="text-gray-600">Loading…</p>
//       </div>
//     );
//   }

//   if (err) {
//     return (
//       <div className="max-w-5xl mx-auto p-6">
//         <h1 className="text-2xl font-bold mb-4">Your Orders</h1>
//         <p className="text-red-600">{err}</p>
//         <Link href="/" className="text-indigo-600 hover:underline mt-4 inline-block">
//           Continue shopping
//         </Link>
//       </div>
//     );
//   }

//   return (
//     <div className="max-w-5xl mx-auto p-6">
//       <div className="flex items-baseline justify-between mb-6">
//         <h1 className="text-2xl font-bold">Your Orders</h1>
//         <Link href="/" className="text-sm text-indigo-600 hover:underline">Continue shopping</Link>
//       </div>

//       {orders.length === 0 ? (
//         <div className="rounded border p-6 bg-white">
//           <p className="text-gray-700">You don’t have any orders yet.</p>
//         </div>
//       ) : (
//         <div className="space-y-6">
//           {orders.map((o) => (
//             <div key={o.order_id} className="rounded border p-5 bg-white shadow-sm">
//               <div className="flex flex-wrap items-center justify-between gap-3">
//                 <div>
//                   <p className="text-sm text-gray-500">Order #</p>
//                   <p className="font-semibold">{o.order_id}</p>
//                 </div>
//                 <div>
//                   <p className="text-sm text-gray-500">Placed</p>
//                   <p className="font-medium">{o.order_date ? new Date(o.order_date).toLocaleString() : '—'}</p>
//                 </div>
//                 <div>
//                   <p className="text-sm text-gray-500">Status</p>
//                   <p className="font-medium capitalize">{o.status || '—'}</p>
//                 </div>
//                 <div>
//                   <p className="text-sm text-gray-500">Total</p>
//                   <p className="font-semibold">${o.total_amount.toFixed(2)}</p>
//                 </div>
//               </div>

//               <div className="mt-4 divide-y">
//                 {o.items.map((it) => (
//                   <div key={it.order_item_id} className="py-3 flex items-center justify-between">
//                     <div>
//                       <p className="font-medium">{it.product_name || `Product #${it.product_id}`}</p>
//                       <p className="text-sm text-gray-600">Qty: {it.quantity}</p>
//                     </div>
//                     <div className="text-right">
//                       <p className="text-sm text-gray-500">Unit</p>
//                       <p className="font-medium">${it.price.toFixed(2)}</p>
//                     </div>
//                   </div>
//                 ))}
//               </div>

//               {/* Optional: link to a future order detail page */}
//               {/* <Link href={`/orders/${o.order_id}`} className="text-sm text-indigo-600 hover:underline mt-3 inline-block">
//                 View details
//               </Link> */}
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }
