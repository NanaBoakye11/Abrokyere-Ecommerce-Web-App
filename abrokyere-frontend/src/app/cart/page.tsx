'use client';

import { useEffect, useState, useCallback } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface CartItem {
  cart_item_id: string;
  product_name: string;
  price: number;                // unit or line price is fine; backend returns total_amount separately
  quantity: number;
  product_image_url?: string;   // optional, shown if present
}

export default function CartPage() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [checkingOut, setCheckingOut] = useState<boolean>(false);
  const router = useRouter();

  const fetchCart = useCallback(async () => {
    try {
      setLoading(true);
      const res = await api.get('/cart/');
      setCartItems(res.data.items || []);
      setTotalAmount(res.data.total_amount || 0);
    } catch (error) {
      console.error('❌ Failed to fetch cart:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // simple auth guard (relies on your localStorage session)
    const token = localStorage.getItem('token');
    const loginTimestamp = localStorage.getItem('loginTimestamp');

    const twoDays = 2 * 24 * 60 * 60 * 1000;
    const isExpired =
      !token ||
      !loginTimestamp ||
      Date.now() - parseInt(loginTimestamp, 10) > twoDays;

    if (isExpired) {
      router.push('/login');
      return;
    }

    fetchCart();
  }, [fetchCart, router]);

  const updateQuantity = async (itemId: string, newQty: number) => {
    if (newQty < 1) return;
    try {
      await api.patch('/cart/update-item/', {
        cart_item_id: itemId,
        quantity: newQty,
      });
      await fetchCart();
    } catch (error) {
      console.error('❌ Failed to update quantity:', error);
    }
  };

  const removeItem = async (itemId: string) => {
    try {
      await api.delete(`/cart/remove-item/${itemId}/`);
      await fetchCart();
    } catch (error) {
      console.error('❌ Failed to remove item:', error);
    }
  };

  const handleCheckout = async () => {
    try {
      setCheckingOut(true);
      // Using your axios instance (it already adds the JWT)
      const { data } = await api.post('/checkout/create-session/');
      if (!data?.url) throw new Error('No checkout URL returned');
      window.location.href = data.url; // Redirect to Stripe Checkout
    } catch (e: any) {
      console.error('Checkout error:', e);
      alert(e?.response?.data?.error || e?.message || 'Could not start checkout');
      setCheckingOut(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-2xl font-bold mb-6">Your Shopping Cart</h1>
        <p className="text-gray-600">Loading…</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Shopping Cart</h1>

      {cartItems.length === 0 ? (
        <p className="text-gray-600">Your cart is empty.</p>
      ) : (
        <div className="grid md:grid-cols-3 gap-8">
          {/* Left: Cart items */}
          <div className="md:col-span-2 space-y-6">
            {cartItems.map((item) => (
              <div
                key={item.cart_item_id}
                className="flex gap-4 border-b pb-4 items-center"
              >
                {/* Product image */}
                <div className="w-24 h-24 bg-gray-100 flex items-center justify-center rounded overflow-hidden">
                  {item.product_image_url ? (
                    <Image
                      src={item.product_image_url}
                      alt={item.product_name}
                      width={96}
                      height={96}
                      className="object-cover"
                    />
                  ) : (
                    <span className="text-sm text-gray-500">No Image</span>
                  )}
                </div>

                {/* Details */}
                <div className="flex-1">
                  <h3 className="font-semibold">{item.product_name}</h3>
                  <p className="text-gray-600 text-sm">${item.price}</p>

                  {/* Quantity controls */}
                  <div className="flex items-center gap-2 mt-2">
                    <button
                      onClick={() =>
                        item.quantity > 1 &&
                        updateQuantity(item.cart_item_id, item.quantity - 1)
                      }
                      className="px-2 py-1 border rounded text-sm"
                    >
                      –
                    </button>
                    <span className="font-medium">{item.quantity}</span>
                    <button
                      onClick={() =>
                        updateQuantity(item.cart_item_id, item.quantity + 1)
                      }
                      className="px-2 py-1 border rounded text-sm"
                    >
                      +
                    </button>
                  </div>

                  {/* Remove */}
                  <button
                    onClick={() => removeItem(item.cart_item_id)}
                    className="text-red-500 text-sm mt-2 hover:underline"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Right: Order summary */}
          <div className="border p-6 rounded shadow-sm bg-white space-y-4 h-fit">
            <h2 className="text-lg font-semibold border-b pb-2">Order Summary</h2>
            <div className="flex justify-between">
              <span>Subtotal</span>
              <span>${totalAmount.toFixed(2)}</span>
            </div>
            <p className="text-sm text-gray-500">
              Shipping and taxes calculated at checkout.
            </p>
            <button
              onClick={handleCheckout}
              disabled={checkingOut}
              className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {checkingOut ? 'Redirecting…' : 'Proceed to Checkout'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}







// 'use client';

// import { useEffect, useState } from 'react';
// import api from '@/lib/api';
// import Image from 'next/image';
// import { useRouter } from 'next/navigation';

// interface CartItem {
//   cart_item_id: string;
//   product_name: string;
//   price: number;
//   quantity: number;
//   product_image_url?: string;
// }

// export default function CartPage() {
//   const [cartItems, setCartItems] = useState<CartItem[]>([]);
//   const [totalAmount, setTotalAmount] = useState<number>(0);
//   const router = useRouter();

//   useEffect(() => {
//     fetchCart();
//   }, []);

//   const fetchCart = async () => {
//     try {
//       const res = await api.get('/cart/');
//       setCartItems(res.data.items || []);
//       setTotalAmount(res.data.total_amount || 0);
//     } catch (error) {
//       console.error('❌ Failed to fetch cart:', error);
//     }
//   };

//   const updateQuantity = async (itemId: string, newQty: number) => {
//     try {
//       await api.patch('/cart/update-item/', {
//         cart_item_id: itemId,
//         quantity: newQty,
//       });
//       fetchCart();
//     } catch (error) {
//       console.error('❌ Failed to update quantity:', error);
//     }
//   };

//   const removeItem = async (itemId: string) => {
//     try {
//       await api.delete(`/cart/remove-item/${itemId}/`);
//       fetchCart();
//     } catch (error) {
//       console.error('❌ Failed to remove item:', error);
//     }
//   };

//   return (
//     <div className="max-w-6xl mx-auto p-6">
//       <h1 className="text-2xl font-bold mb-6">Your Shopping Cart</h1>

//       {cartItems.length === 0 ? (
//         <p className="text-gray-600">Your cart is empty.</p>
//       ) : (
//         <div className="grid md:grid-cols-3 gap-8">
//           {/* Left: Cart items */}
//           <div className="md:col-span-2 space-y-6">
//             {cartItems.map((item) => (
//               <div
//                 key={item.cart_item_id}
//                 className="flex gap-4 border-b pb-4 items-center"
//               >
//                 <div className="w-24 h-24 bg-gray-100 flex items-center justify-center rounded overflow-hidden">
//                   {item.product_image_url ? (
//                     <Image
//                       src={item.product_image_url}
//                       alt={item.product_name}
//                       width={96}
//                       height={96}
//                       className="object-cover"
//                     />
//                   ) : (
//                     <span className="text-sm text-gray-500">No Image</span>
//                   )}
//                 </div>

//                 <div className="flex-1">
//                   <h3 className="font-semibold">{item.product_name}</h3>
//                   <p className="text-gray-600 text-sm">${item.price}</p>

//                   <div className="flex items-center gap-2 mt-2">
//                     <button
//                       onClick={() =>
//                         item.quantity > 1 && updateQuantity(item.cart_item_id, item.quantity - 1)
//                       }
//                       className="px-2 py-1 border rounded text-sm"
//                     >
//                       –
//                     </button>
//                     <span className="font-medium">{item.quantity}</span>
//                     <button
//                       onClick={() => updateQuantity(item.cart_item_id, item.quantity + 1)}
//                       className="px-2 py-1 border rounded text-sm"
//                     >
//                       +
//                     </button>
//                   </div>

//                   <button
//                     onClick={() => removeItem(item.cart_item_id)}
//                     className="text-red-500 text-sm mt-2 hover:underline"
//                   >
//                     Remove
//                   </button>
//                 </div>
//               </div>
//             ))}
//           </div>

//           {/* Right: Order summary */}
//           <div className="border p-6 rounded shadow-sm bg-white space-y-4">
//             <h2 className="text-lg font-semibold border-b pb-2">Order Summary</h2>
//             <div className="flex justify-between">
//               <span>Subtotal</span>
//               <span>${totalAmount.toFixed(2)}</span>
//             </div>
//             <p className="text-sm text-gray-500">Shipping and tax calculated at checkout.</p>
//               <button
//                 onClick={async () => {
//                   try {
//                     const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/checkout/create-session/`, {
//                       method: 'POST',
//                       headers: {
//                         'Content-Type': 'application/json',
//                         // your axios interceptor already adds the token globally,
//                         // but fetch doesn't—so add it here from localStorage:
//                         Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
//                       },
//                       credentials: 'include',
//                     });

//                     const data = await res.json();
//                     if (!res.ok) throw new Error(data?.error || 'Failed to create checkout session');

//                     window.location.href = data.url; // redirect to Stripe Checkout
//                   } catch (e: any) {
//                     console.error('Checkout error:', e);
//                     alert(e?.message || 'Could not start checkout');
//                   }
//                 }}
//                 className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
//               >
//                 Proceed to Checkout
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }


/* <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
              Proceed to Checkout
</button> */


// interface CartItem {
//   cart_item_id: string;
//   product_name: string;
//   quantity: number;
//   price: number;
//   image_url?: string; // Optional: adjust based on your API response
// }

// export default function CartPage() {
//   const [cartItems, setCartItems] = useState<CartItem[]>([]);
//   const [totalAmount, setTotalAmount] = useState<number>(0);
//   const router = useRouter();

//   useEffect(() => {
//     const fetchCart = async () => {
//       try {
//         const res = await api.get('/cart/');
//         setCartItems(res.data.items || []);
//         setTotalAmount(res.data.total_amount || 0);
//       } catch (err) {
//         console.error('Error loading cart:', err);
//       }
//     };

//     fetchCart();
//   }, []);

//   return (
//     <div className="max-w-7xl mx-auto px-4 py-10">
//       <h1 className="text-3xl font-bold mb-8">Your Cart</h1>

//       {cartItems.length === 0 ? (
//         <p className="text-gray-600">Your cart is empty.</p>
//       ) : (
//         <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
//           {/* Left: Cart Items */}
//           <div className="md:col-span-2 space-y-6">
//             {cartItems.map((item) => (
//               <div
//                 key={item.cart_item_id}
//                 className="flex items-center border rounded-lg p-4 shadow-sm"
//               >
//                 {item.image_url ? (
//                   <Image
//                     src={item.image_url}
//                     alt={item.product_name}
//                     width={80}
//                     height={80}
//                     className="rounded-md object-cover"
//                   />
//                 ) : (
//                   <div className="w-20 h-20 bg-gray-200 rounded-md flex items-center justify-center text-gray-500">
//                     No Image
//                   </div>
//                 )}

//                 <div className="ml-4 flex-1">
//                   <h3 className="text-lg font-semibold">{item.product_name}</h3>
//                   <p className="text-sm text-gray-600">Qty: {item.quantity}</p>
//                   <p className="text-sm text-gray-600">${item.price.toFixed(2)}</p>
//                 </div>
//               </div>
//             ))}
//           </div>

//           {/* Right: Order Summary */}
//           <div className="bg-gray-50 border rounded-lg p-6 shadow-md h-fit">
//             <h2 className="text-lg font-semibold mb-4">Order Summary</h2>
//             <div className="flex justify-between mb-2">
//               <span>Subtotal</span>
//               <span>${totalAmount.toFixed(2)}</span>
//             </div>
//             <p className="text-sm text-gray-500 mb-6">
//               Shipping and taxes calculated at checkout.
//             </p>
//             <button
//               onClick={() => router.push('/checkout')}
//               className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
//             >
//               Proceed to Checkout
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }




// 'use client';

// import { useEffect, useState } from 'react';
// import { useRouter } from 'next/navigation';
// import api from '@/lib/api';

// interface CartItem {
//   cart_item_id: string;
//   product_name: string;
//   quantity: number;
//   price: number;
// }

// export default function CartPage() {
//   const [cartItems, setCartItems] = useState<CartItem[]>([]);
//   const [totalAmount, setTotalAmount] = useState<number>(0);
//   const [loading, setLoading] = useState(true);
//   const router = useRouter();

//   useEffect(() => {
//     const token = localStorage.getItem('token');
//     const loginTimestamp = localStorage.getItem('loginTimestamp');

//     if (!token || !loginTimestamp || Date.now() - parseInt(loginTimestamp) > 2 * 24 * 60 * 60 * 1000) {
//       router.push('/login');
//       return;
//     }

//     api.get('/cart/')
//       .then(res => {
//         setCartItems(res.data.items || []);
//         setTotalAmount(res.data.total_amount || 0);
//         setLoading(false);
//       })
//       .catch(err => {
//         console.error('Error fetching cart:', err);
//         router.push('/login');
//       });
//   }, []);

//   if (loading) return <div className="p-6">Loading cart...</div>;

//   return (
//     <div className="max-w-4xl mx-auto px-4 py-8">
//       <h1 className="text-2xl font-semibold mb-6">Your Shopping Cart</h1>

//       {cartItems.length === 0 ? (
//         <p className="text-gray-600">Your cart is empty.</p>
//       ) : (
//         <div className="bg-white shadow rounded-lg p-4 space-y-4">
//           {cartItems.map(item => (
//             <div key={item.cart_item_id} className="flex justify-between border-b pb-3">
//               <div>
//                 <p className="font-semibold text-gray-800">{item.product_name}</p>
//                 <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
//               </div>
//               <p className="font-medium text-gray-700">${item.price.toFixed(2)}</p>
//             </div>
//           ))}

//           <div className="flex justify-between pt-4 border-t font-semibold text-lg">
//             <span>Total:</span>
//             <span>${totalAmount.toFixed(2)}</span>
//           </div>

//           <div className="mt-6">
//             <button
//               onClick={() => router.push('/checkout')}
//               className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition"
//             >
//               Proceed to Checkout
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }
