from rest_framework import serializers
from core.models import Products, Categories, ProductImages


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image_url', 'is_main', 'alt_text']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_id', 'category_name']

class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Products
        fields = [
            'product_id',
            'product_name',
            'price',
            'description',
            'prod_reviews',
            'category',
            'featured',
            'product_images'
        ]