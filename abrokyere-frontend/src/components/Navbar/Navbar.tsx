'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface Customer {
  first_name: string;
  last_name: string;
  email: string;
}

export default function Navbar() {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkSession = () => {
        const token = localStorage.getItem('token');
        const storedCustomer = localStorage.getItem('customer');
        const loginTimestamp = localStorage.getItem('loginTimestamp');

        console.log("Token1:", token);
        console.log("Customer1:", storedCustomer);
        console.log("LoginStamp1:", loginTimestamp);

    
        if (token && storedCustomer && loginTimestamp) {
          const oneDay = 24 * 60 * 60 * 1000;
          const loggedInAt = parseInt(loginTimestamp);
          const now = Date.now();
    
          try {
            const parsedCustomer = JSON.parse(storedCustomer);
            if (parsedCustomer && typeof parsedCustomer === 'object') {
                if (now - loggedInAt < oneDay) {
                  setCustomer(parsedCustomer);
                } else {
                  localStorage.clear();
                  setCustomer(null);
                }
              } else {
                throw new Error('Parsed customer is not an object');
              }
          } catch (err) {
            console.error('❌ Failed to parse customer');
            localStorage.clear();
            setCustomer(null);
          }
        } else {
          setCustomer(null);
        }
      };
    
      // ✅ Run once
      checkSession();
    
      // ✅ Run again when login fires `storage-update`
      window.addEventListener('storage-update', checkSession);
    
      return () => {
        window.removeEventListener('storage-update', checkSession);
      };
    }, []);

  const handleSignOut = () => {
    localStorage.clear();
    setCustomer(null);
    router.push('/login');
  };

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        {/* Left - Logo & Links */}
        <div className="flex items-center gap-6">
          <Link href="/" className="text-2xl font-bold text-gray-900 tracking-tight">
            Abrokyere
          </Link>
          <div className="hidden md:flex gap-4 text-sm text-gray-700 font-medium">
            <Link href="/">Home</Link>
            <Link href="/about">About</Link>
            <Link href="/categories">Categories</Link>
          </div>
        </div>

        {/* Right - Auth Info */}
        <div className="flex items-center gap-6 text-sm font-medium text-gray-700">
          {customer ? (
            <>
              <div className="text-right leading-tight">
                <p className="text-xs text-gray-500">Welcome back,</p>
                <p className="font-semibold text-black">{customer.first_name}</p>
              </div>
              <Link href="/account" className="hover:underline">Account</Link>
              <Link href="/orders" className="hover:underline">Orders</Link>
              <button
                onClick={handleSignOut}
                className="text-red-600 hover:underline"
              >
                Sign Out
              </button>
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
