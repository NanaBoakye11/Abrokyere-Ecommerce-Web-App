// src/types/product.ts
export interface ProductImage {
  image_id: number;
  image_url: string;
  is_main: boolean;
  alt_text?: string;
}


export interface Product {
    product_id: number;
    product_name: string;
    price: number;
    description: string;
    prod_reviews?: string;
    product_images?: ProductImage[];
    category?: {
      category_id: number;
      category_name: string;
    };
  }
  