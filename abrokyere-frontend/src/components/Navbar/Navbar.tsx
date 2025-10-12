'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ShoppingCart } from 'lucide-react';
import axios from 'axios';
import api from '@/lib/api';


interface Customer {
  first_name: string;
  last_name: string;
  email: string;
}


interface CartItem {
  cart_item_id: string;
  product_name: string;
  quantity: number;
  price: number;
}


export default function Navbar() {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [showCart, setShowCart] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkSession = () => {
      try {
        const token = localStorage.getItem('token');
        const storedCustomer = localStorage.getItem('customer');
        const loginTimestamp = localStorage.getItem('loginTimestamp');

        if (token && storedCustomer && loginTimestamp) {
          const twoDays = 2 * 24 * 60 * 60 * 1000;
          const loggedInAt = parseInt(loginTimestamp);
          const now = Date.now();

          if (now - loggedInAt < twoDays) {
            const parsedCustomer = JSON.parse(storedCustomer);
            if (parsedCustomer && typeof parsedCustomer === 'object') {
              setCustomer(parsedCustomer);
              fetchCartItems(token);
              return;
            }
          }
        }

        localStorage.clear();
        setCustomer(null);
        setCartItems([]);
        setTotalAmount(0);


      } catch (err) {
        console.error('❌ Session check failed:', err);
        localStorage.clear();
        setCustomer(null);
        setCartItems([]);
        setTotalAmount(0);
      }
    };

    checkSession();

    // Allow other components to refresh session display
    window.addEventListener('storage-update', checkSession);
    return () => window.removeEventListener('storage-update', checkSession);
  }, []);


  const fetchCartItems = async (token: string) => {
    try {
      console.log("🪪 Token being sent:", token);
      const res = await api.get('/cart/');

      setCartItems(res.data.items || []);
      setTotalAmount(res.data.total_amount || 0); // <-- ADD THIS

    } catch (error) {
      console.error('❌ Failed to fetch cart:', error);
    }
  };

  const handleSignOut = () => {
    localStorage.clear();
    setCustomer(null);
    setCartItems([]);
    setTotalAmount(0);
    router.push('/login');
  };

  return (
 <nav className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        {/* Left side logo + links */}
        <div className="flex items-center gap-6">
          <Link href="/" className="text-2xl font-bold text-gray-900 tracking-tight">Abrokyere</Link>
          <div className="hidden md:flex gap-4 text-sm text-gray-700 font-medium">
            <Link href="/">Home</Link>
            <Link href="/about">About</Link>
            <Link href="/categories">Categories</Link>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-6 text-sm font-medium text-gray-700">
          {customer ? (
            <>
              <div className="text-right leading-tight">
                <p className="text-xs text-gray-500">Welcome back,</p>
                <p className="font-semibold text-black">{customer.first_name}</p>
              </div>
              <Link href="/account" className="hover:underline">Account</Link>
              <Link href="/orders" className="hover:underline">Orders</Link>

              {/* Cart */}
              <div className="relative">
                <button
                  onClick={() => setShowCart(!showCart)}
                  className="relative cursor-pointer hover:opacity-80"
                >
                  <ShoppingCart className="w-6 h-6" />
                  {cartItems.length > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full px-1">
                      {cartItems.length}
                    </span>
                  )}
                </button>

                {showCart && (
                  <div className="absolute right-0 mt-2 w-80 bg-white border rounded-lg shadow-lg z-50 p-4 max-h-80 overflow-y-auto">
                    <p className="font-bold text-sm mb-2 border-b pb-1">Your Cart</p>
                    {cartItems.length === 0 ? (
                      <p className="text-sm text-gray-600">Your cart is empty</p>
                    ) : (
                      <>
                        {cartItems.map((item) => (
                          <div key={item.cart_item_id} className="border-b py-2">
                            <p className="font-semibold">{item.product_name}</p>
                            <p className="text-sm text-gray-600">Qty: {item.quantity}</p>
                            <p className="text-sm text-gray-600">${item.price}</p>
                          </div>
                        ))}

                        <div className="mt-4 pt-2 border-t flex justify-between font-semibold text-sm">
                          <span>Total:</span>
                          <span>${totalAmount.toFixed(2)}</span>
                        </div>

                        <button
                          onClick={() => {
                            setShowCart(false);
                            router.push('/cart');
                          }}
                          className="mt-3 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 text-sm"
                        >
                          Go to Cart
                        </button>
                      </>
                    )}
                  </div>
                )}
              </div>

              <button onClick={handleSignOut} className="text-red-600 hover:underline">Sign Out</button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-blue-600 hover:underline">Sign In</Link>
              <Link href="/register" className="hover:underline text-gray-700">New Customer?</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}



 