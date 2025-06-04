from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Products, Categories
from core.serializers.product_serializer import ProductSerializer
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404



class FeaturedProductsView(APIView):
    def get(self, request):
        featured_products = Products.objects.filter(featured=True).annotate(
            calculated_rating_average=Avg('reviews__rating'),
            calculated_rating_count=Count('reviews')
        )
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByCategoryView(APIView):
    def get(self, request, category_id):
        products = Products.objects.filter(category_id=category_id).annotate(
            calculated_rating_average=Avg('reviews__rating'),
            calculated_rating_count=Count('reviews')
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    


class ProductsGroupedByCategory(APIView):
    def get(self, request):
        categories = Categories.objects.all()
        data = []

        for category in categories:
            # products = Products.objects.filter(category=category)[:10]
            products = Products.objects.filter(category=category).annotate(
                calculated_rating_average=Avg('reviews__rating'),
                calculated_rating_count=Count('reviews')
            )[:10]
            serializer = ProductSerializer(products, many=True)
            data.append({
                'category_id': category.category_id,
                'category_name': category.category_name,
                'products': serializer.data
            })

        return Response(data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Products, product_id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)