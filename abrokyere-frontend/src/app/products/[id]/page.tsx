'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Product } from '@/types/product';
import { Customer } from '@/types/customer';
import axios from 'axios';
import {fetchProductById, addToCart} from '@/lib/api';


export default function ProductDetailPage() {
  const { id } = useParams();
  const router = useRouter();

  const [product, setProduct] = useState<Product | null>(null);
  const customerId = localStorage.getItem('customer_id'); // or however you're storing it
  const [qty, setQty] = useState(1);


  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchProductById(id as string);
        setProduct(res.data);
      } catch (err) {
        console.error('Failed to load product', err);
      }
    };

    if (id) load();
  }, [id]);

  if (!product) return <div className="p-6">Loading...</div>;

  const mainImage = product.product_images?.find(img => img.is_main);

                    //Add to Cart // 
const handleAddToCart = async () => {
    try{
        await addToCart({ 
          // customer_id: customerId,
          product_id: product.product_id, 
          quantity: qty
        });
        console.log("Adding to CART");
        router.refresh();

        // router.push('/cart');
    } catch (err) {
        console.error('Failed to add to cart', err);
    }
};

  return (
    <div className="p-6 max-w-4xl mx-auto bg-white rounded shadow">
      {mainImage && (
        <img src={mainImage.image_url} alt={mainImage.alt_text || product.product_name} className="w-full h-96 object-cover mb-4" />
      )}
      <h1 className="text-3xl font-bold mb-2">{product.product_name}</h1>
      <p className="text-xl text-green-700 font-semibold mb-1">${product.price}</p>
      <p className="text-sm text-gray-600 mb-4">{product.description}</p>
<div className="mt-6 flex items-center gap-3">
  <input
    type="number"
    min={1}
    value={qty}
    onChange={(e) => setQty(parseInt(e.target.value))}
    className="w-20 border rounded px-2 py-1"
  />
  <button
    onClick={handleAddToCart}
    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
  >
    Add to Cart
  </button>
</div>
    </div>
  );
}