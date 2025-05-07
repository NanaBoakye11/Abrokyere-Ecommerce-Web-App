from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Products
from core.serializers.product_serializer import ProductSerializer

class FeaturedProductsView(APIView):
    def get(self, request):
        featured_products = Products.objects.filter(featured=True)  # Adjust number as needed
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByCategoryView(APIView):
    def get(self, request, category_id):
        products = Products.objects.filter(category_id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)