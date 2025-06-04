from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.cart_service import add_item_to_cart
from django.utils import timezone
from core.models import Carts, CartItems, Products, Inventory, Stores
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from django.db import transaction


class AddToCartView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        if not all([customer_id, product_id]):
            return Response({'error': 'customer_id and product_id are required.'}, status=400)

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        store = Stores.objects.first()
        if not store:
            return Response({'error': 'Store not configured'}, status=500)

        with transaction.atomic():
            try:
                inventory = Inventory.objects.select_for_update().get(product=product, store=store)
            except Inventory.DoesNotExist:
                return Response({"error": "Inventory not found for this product."}, status=404)

            if inventory.quantity < quantity:
                return Response({"error": "Not enough inventory."}, status=400)

            inventory.quantity -= quantity
            inventory.save()

            cart = Carts.objects.filter(customer_id=customer_id, status='active').first()
            if not cart:
                cart = Carts.objects.create(
                    customer_id=customer_id,
                    status='active',
                    total_qty=0,
                    total_amount=Decimal('0.00')
                )

            cart_item, created = CartItems.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity, 'price': product.price}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            cart.total_qty = sum(item.quantity for item in cart.cartitems_set.all())
            cart.total_amount = sum(item.quantity * item.price for item in cart.cartitems_set.all())
            cart.save()

        return Response({'message': 'Added to cart'}, status=200)







