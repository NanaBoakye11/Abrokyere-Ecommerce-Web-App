// src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { fetchFeaturedProducts, fetchGroupedProducts } from '@/lib/api';
import { Product } from '@/types/product';
import Link from 'next/link';



export default function HomePage() {
  const [featured, setFeatured] = useState<Product[]>([]);
  const [grouped, setGrouped] = useState<any[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [featuredRes, groupedRes] = await Promise.all([
          fetchFeaturedProducts(),
          fetchGroupedProducts()
        ]);
          setFeatured(featuredRes.data);
          setGrouped(groupedRes.data);
      } catch (err) {
        console.error('Fetch error', err);
      }
    };

    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 px-6 pt-8">
      {/* 🔸 Featured Product Slider */}
      <section className="mb-10">
        <h1 className="text-4xl font-extrabold text-center mb-4">Explore Featured</h1>
        <div className="overflow-x-auto flex gap-4 snap-x">
          {featured.map((product) => {
            const img = product.product_images?.find((i) => i.is_main);
            return (
              <Link key={product.product_id} href={`/products/${product.product_id}`}>
                  <div className="min-w-[300px] snap-start bg-white rounded shadow p-4">
                  {img && <img src={img.image_url} className="h-48 w-full object-cover mb-2" />}
                  <h2 className="font-semibold">{product.product_name}</h2>
                  <p>${product.price}</p>
              </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* 🔸 Grouped by Category */}
      <section>
        {grouped.map((group) => (
          <div key={group.category_id} className="mb-10">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-2xl font-bold">{group.category_name}</h2>
              <a href={`/products/category/${group.category_id}`} className="text-blue-600 text-sm">View All</a>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {group.products.map((product) => {
                const img = product.product_images?.find((i) => i.is_main);
                return (
                  <Link key={product.product_id} href={`/products/${product.product_id}`}>
                  <div className="bg-white p-3 rounded shadow">
                    {img && <img src={img.image_url} className="h-40 w-full object-cover mb-2" />}
                    <h3 className="font-medium">{product.product_name}</h3>
                    <p>${product.price}</p>
                  </div>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}











// export default function HomePage() {
//   const [products, setProducts] = useState<Product[]>([]);

//   useEffect(() => {
//     const load = async () => {
//       try {
//         const res = await fetchFeaturedProducts();
//         console.log('PRODUCT RESPONSE 📦',res.data);
//         const data = res.data as Product[]; // ✅ Type assertion
//         setProducts(data);
//       } catch (err) {
//         console.error('Error fetching featured products:', err);
//       }
//     };

//     load();
//   }, []);

//   return (
//     <div className="min-h-screen bg-gray-50 text-gray-900 p-8">
//       <h1 className="text-4xl font-extrabold text-center mb-4">Explore Featured Products</h1>
//       <p className="text-center text-gray-950 mb-8">Shop the latest & trending items now</p>
  
//       <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
//         {products.map((product) => {
//           const mainImage = product.product_images?.find((img) => img.is_main);
  
//           return (
//             <div key={product.product_id} className="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition">
//               {mainImage && (
//                 <img
//                   src={mainImage.image_url}
//                   alt={mainImage.alt_text || product.product_name}
//                   className="w-full h-48 object-cover rounded mb-3"
//                 />
//               )}
//               <h2 className="text-gray-900 font-bold text-lg mb-1">{product.product_name}</h2>
//               <p className="text-gray-900 font-medium mb-1">${product.price}</p>
//               <p className="text-sm text-gray-950 ">{product.description}</p>
//             </div>
//           );
//         })}
//       </div>
//     </div>
//   );
  


  
// }


