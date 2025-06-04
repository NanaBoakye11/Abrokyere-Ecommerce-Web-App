from rest_framework import serializers
from core.models import Products, Categories, ProductImages, ProductReviews


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = ['rating', 'review_text', 'created_at']

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
    rating_average = serializers.FloatField()
    rating_count = serializers.IntegerField()

    class Meta:
        model = Products
        fields = [
            'product_id',
            'product_name',
            'price',
            'description',
            'prod_reviews',
            'rating_average',    
            'rating_count',
            'category',
            'featured',
            'product_images'
        ]