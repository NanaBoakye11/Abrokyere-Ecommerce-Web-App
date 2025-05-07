// src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { fetchFeaturedProducts } from '@/lib/api';
import { Product } from '@/types/product';

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchFeaturedProducts();
        console.log('PRODUCT RESPONSE 📦',res.data);
        const data = res.data as Product[]; // ✅ Type assertion
        setProducts(data);
      } catch (err) {
        console.error('Error fetching featured products:', err);
      }
    };

    load();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8">
      <h1 className="text-4xl font-extrabold text-center mb-4">Explore Featured Products</h1>
      <p className="text-center text-gray-950 mb-8">Shop the latest & trending items now</p>
  
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => {
          const mainImage = product.product_images?.find((img) => img.is_main);
  
          return (
            <div key={product.product_id} className="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition">
              {mainImage && (
                <img
                  src={mainImage.image_url}
                  alt={mainImage.alt_text || product.product_name}
                  className="w-full h-48 object-cover rounded mb-3"
                />
              )}
              <h2 className="text-gray-900 font-bold text-lg mb-1">{product.product_name}</h2>
              <p className="text-gray-900 font-medium mb-1">${product.price}</p>
              <p className="text-sm text-gray-950 ">{product.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
  



  // return (
  //   <div className="p-8">
  //     <h1 className="text-3xl font-bold mb-6">Featured Products</h1>
  //     <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
  //       {products.map((product) => {
  //         const mainImage = product.product_images?.find((img) => img.is_main);
  
  //         return (

  //           <div key={product.product_id} className="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition">
  //             {mainImage && (
  //               <img
  //                 src={mainImage.image_url}
  //                 alt={mainImage.alt_text || product.product_name}
  //                 className="w-full h-48 object-cover rounded mb-3"
  //               />
  //             )}
  //             <h2 className="text-gray-950 font-bold text-lg mb-1">{product.product_name}</h2>
  //             <p className="text-gray-950 font-medium mb-1">${product.price}</p>
  //             <p className="text-sm text-gray-950">{product.description}</p>
  //           </div>
  //         );
  //       })}
  //     </div>
  //   </div>
  // );
}






// return (
//   <div className="p-8">
//     <h1 className="text-3xl font-bold mb-6">Featured Products</h1>
//     <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
//       {products.map((product) => (
//         <div key={product.product_id} className="border rounded-xl p-4 shadow hover:shadow-lg transition">
//           <h2 className="font-semibold text-lg">{product.product_name}</h2>
//           <p className="text-gray-500">${product.price}</p>
//           <p className="text-sm text-gray-700">{product.description}</p>
//         </div>
//       ))}
//     </div>
//   </div>
// );

// import Image from "next/image";


// // src/app/page.tsx

// export default function Home() {
//   return (
//     <main className="p-6 text-center">
//       <h1 className="text-3xl font-bold">Welcome to Abrokyere!</h1>
//       <p className="mt-2 text-gray-600">Frontend + Backend is working 🎉</p>
//     </main>
//   );
// }


