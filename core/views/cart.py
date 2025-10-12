from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.services.cart_service import add_item_to_cart
from django.utils import timezone
from core.models import Carts, CartItems, Products, Inventory, Stores, Customers
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from core.services.cart_service import add_item_to_cart
from rest_framework.permissions import AllowAny # Crucial for guest carts
from rest_framework_simplejwt.authentication import JWTAuthentication # Add this
from core.serializers.cart import CartSerializer, CartItemCreateSerializer
from django.db.models import Sum




class AddToCartView(APIView):
    authentication_classes = [JWTAuthentication] # Apply JWT authentication
    permission_classes = [AllowAny] # Allow both authenticated and unauthenticated

    def post(self, request, *args, **kwargs):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        customer = None
        if request.user.is_authenticated:
            try:
                # request.user.id will now directly give you the customer_id from the JWT
                # customer_id_from_token = request.user.id
                # customer = Customers.objects.get(customer_id=customer_id_from_token)
                # print(f"DEBUG: Found Customers instance for ID {customer_id_from_token}: {customer.email}")
                customer = request.user.customer
                print(f"DEBUG: Authenticated as: {customer.email}")


                cart, created = Carts.objects.get_or_create(customer=customer, status='active')
                print(f"DEBUG: Cart found/created for customer {customer.customer_id}. Created: {created}")

            except Customers.DoesNotExist:
                # print(f"ERROR: Customers object not found in DB for ID: {customer_id_from_token}")
                return Response({"error": "Customer profile not found for authenticated user."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"ERROR: Unexpected error during authenticated cart add: {e}")
                # Handle cases where JWT is present but invalid/corrupted
                return Response({"error": f"Authentication error: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Guest cart logic (using session_key for persistence)
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key

            try:
                cart = Carts.objects.get(session_key=session_key, customer__isnull=True, status='active')
            except Carts.DoesNotExist:
                cart = Carts.objects.create(session_key=session_key, customer=None, status='active')
            
            # If a guest user was trying to log in but their session expired
            # and they have a session_key, you might want to redirect or prompt login.
            # For simplicity, we just create/get guest cart.

        # Add or update CartItem
        cart_item, item_created = CartItems.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.price = product.price
            cart_item.save()

        cart_items_list = cart.cartitems_set.all()
        cart.total_qty = sum(item.quantity for item in cart_items_list)
        cart.total_amount = sum(item.quantity * item.price for item in cart_items_list)
        cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)



# REAL RECENT 

class CartDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print("🧠 Authenticated user:", request.user)
            print("🧠 Does user have 'customer' attribute?", hasattr(request.user, 'customer'))

            customer = request.user.customer
            cart = Carts.objects.get(customer=customer, status='active')
            items = CartItems.objects.filter(cart=cart)

            data = [
                {
                    "cart_item_id": str(item.cart_item_id),
                    "product_name": item.product.product_name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                }
                for item in items
            ]

            return Response({
                "items": data,
                "total_amount": float(cart.total_amount),  # <-- Just expose this field
                "total_qty": cart.total_qty
            }, status=200)

        except Customers.DoesNotExist:
            return Response({"error": "Customer not found."}, status=404)

        except Carts.DoesNotExist:
            return Response({"items": [], "total_amount": 0.0, "total_qty": 0}, status=200)

        except Exception as e:
            print("🔥 CartDetailView crashed:", str(e))
            return Response({"error": str(e)}, status=500)


class UpdateCartItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        cart_item_id = request.data.get("cart_item_id")
        new_quantity = request.data.get("quantity")

        if not cart_item_id or new_quantity is None:
            return Response({"error": "cart_item_id and quantity are required"}, status=400)

        try:
            customer = request.user.customer
            cart = Carts.objects.get(customer=customer, status="active")
            item = CartItems.objects.get(cart=cart, cart_item_id=cart_item_id)

            item.quantity = new_quantity
            item.price = item.product.price * new_quantity  # update price too
            item.save()

            # 🔁 Recalculate Cart Totals
            totals = CartItems.objects.filter(cart=cart).aggregate(
                total_qty=Sum("quantity"),
                total_amount=Sum("price")
            )

            cart.total_qty = totals["total_qty"] or 0
            cart.total_amount = totals["total_amount"] or 0
            cart.save()

            return Response({
                "message": "Item updated",
                "total_qty": cart.total_qty,
                "total_amount": float(cart.total_amount)
            })

        except CartItems.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)
        except Carts.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)


class RemoveCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, cart_item_id):
        try:
            item = CartItems.objects.get(cart_item_id=cart_item_id, cart__customer=request.user.customer)
            item.delete()
            return Response({"message": "Item removed."}, status=204)
        except CartItems.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)











# class CartDetailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             # Get the authenticated customer's cart
#             customer = request.user.customer
#             cart = Carts.objects.get(customer=customer, status='active')

#             # Use the CartSerializer to return cart details, including cart items and image URLs
#             serializer = CartSerializer(cart, context={'request': request})  # `context` enables absolute URLs if needed
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Carts.DoesNotExist:
#             return Response({
#                 "cart_id": None,
#                 "customer_id": request.user.customer.customer_id if hasattr(request.user, "customer") else None,
#                 "total_qty": 0,
#                 "total_amount": 0.0,
#                 "status": "active",
#                 "cart_items": []
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             print("🔥 CartDetailView crashed:", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CartDetailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             print("🧠 Authenticated user:", request.user)
#             print("🧠 Does user have 'customer' attribute?", hasattr(request.user, 'customer'))

#             customer = request.user.customer  # Will fail if related_name is missing
#             cart = Carts.objects.get(customer=customer, status='active')
#             items = CartItems.objects.filter(cart=cart)

#             data = [
#                 {
#                     "cart_item_id": str(item.cart_item_id),
#                     "product_name": item.product.product_name,
#                     "quantity": item.quantity,
#                     "price": float(item.price),
#                 }
#                 for item in items
#             ]

#             return Response({"items": data}, status=200)

#         except Customers.DoesNotExist:
#             return Response({"error": "Customer not found."}, status=404)

#         except Carts.DoesNotExist:
#             return Response({"items": []}, status=200)

#         except Exception as e:
#             print("🔥 CartDetailView crashed:", str(e))  # <- this will show in terminal
#             return Response({"error": str(e)}, status=500)



# class CartDetailView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             customer = request.user.customer
#             cart = Carts.objects.get(customer=customer, status='active')
#             items = CartItems.objects.filter(cart=cart)

#             # Serialize items
#             data = []
#             for item in items:
#                 data.append({
#                     "cart_item_id": str(item.cart_item_id),
#                     "product_name": item.product.name,
#                     "quantity": item.quantity,
#                     "price": float(item.price),
#                 })

#             return Response({"items": data}, status=200)

#         except Carts.DoesNotExist:
#             return Response({"items": []}, status=200)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)


#MOST RECENT 

# class AddToCartView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = CartItemCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         product_id = serializer.validated_data['product_id']
#         quantity = serializer.validated_data['quantity']

#         customer = None
#         if request.user.is_authenticated:
#             try:
#                 customer_id_from_token = request.user.id
#                 customer = Customers.objects.get(customer_id=customer_id_from_token)
#                 print(f"✅ Authenticated as: {customer.email}")
                
#                 # Use your service function (which will get/create cart)
#                 cart_item = add_item_to_cart(customer.customer_id, product_id, quantity)

#             except Customers.DoesNotExist:
#                 return Response({"error": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Guest session logic
#             session_key = request.session.session_key or request.session.save()
#             try:
#                 cart = Carts.objects.get(session_key=session_key, customer__isnull=True, status='active')
#             except Carts.DoesNotExist:
#                 cart = Carts.objects.create(session_key=session_key, customer=None, status='active')

#             product = Products.objects.get(product_id=product_id)
#             cart_item, _ = CartItems.objects.get_or_create(
#                 cart=cart,
#                 product=product,
#                 defaults={'quantity': quantity, 'price': product.price}
#             )

#         cart = cart_item.cart
#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_200_OK)







# class AddToCartView(APIView):
#     authentication_classes = [JWTAuthentication] # Apply JWT authentication
#     permission_classes = [AllowAny] # Allow both authenticated and unauthenticated

#     def post(self, request, *args, **kwargs):
#         serializer = CartItemCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         product_id = serializer.validated_data['product_id']
#         quantity = serializer.validated_data['quantity']

#         try:
#             product = Products.objects.get(product_id=product_id)
#         except Products.DoesNotExist:
#             return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

#         customer = None
#         if request.user.is_authenticated:
#             try:
#                 # request.user.id will now directly give you the customer_id from the JWT
#                 customer_id_from_token = request.user.id
#                 customer = Customers.objects.get(customer_id=customer_id_from_token)
#                 print(f"DEBUG: Found Customers instance for ID {customer_id_from_token}: {customer.email}")
#                 print(f"✅ Authenticated as: {customer.email}")

                
#                 # cart, created = Carts.objects.get_or_create(customer=customer, status='active')
#                 # print(f"DEBUG: Cart found/created for customer {customer.customer_id}. Created: {created}")
                
                
#                 cart_item = add_item_to_cart(customer.customer_id, product_id, quantity)

#             except Customers.DoesNotExist:
#                 print(f"ERROR: Customers object not found in DB for ID: {customer_id_from_token}")
#                 return Response({"error": "Customer profile not found for authenticated user."}, status=status.HTTP_400_BAD_REQUEST)
#             # except Exception as e:
#             #     print(f"ERROR: Unexpected error during authenticated cart add: {e}")
#             #     # Handle cases where JWT is present but invalid/corrupted
#             #     return Response({"error": f"Authentication error: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             # Guest cart logic (using session_key for persistence)
#             session_key = request.session.session_key or request.session.save()
#             if not session_key:
#                 request.session.save()
#                 session_key = request.session.session_key

#             try:
#                 cart = Carts.objects.get(session_key=session_key, customer__isnull=True, status='active')
#             except Carts.DoesNotExist:
#                 cart = Carts.objects.create(session_key=session_key, customer=None, status='active')
            
#             # If a guest user was trying to log in but their session expired
#             # and they have a session_key, you might want to redirect or prompt login.
#             # For simplicity, we just create/get guest cart.

#         # Add or update CartItem
#         cart_item, item_created = CartItems.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={'quantity': quantity, 'price': product.price}
#         )

#         if not item_created:
#             cart_item.quantity += quantity
#             cart_item.price = product.price
#             cart_item.save()

#         cart_items_list = cart.cartitems_set.all()
#         cart.total_qty = sum(item.quantity for item in cart_items_list)
#         cart.total_amount = sum(item.quantity * item.price for item in cart_items_list)
#         cart.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_200_OK)








# class AddToCartView(APIView):
#     def post(self, request):
#         data = request.data
#         product_id = data.get('product_id')
#         quantity = int(data.get('quantity', 1))

#         if not product_id:
#             return Response({'error': 'product_id is required.'}, status=400)

#         # Validate product
#         try:
#             product = Products.objects.get(product_id=product_id)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=404)

#         store = Stores.objects.first()
#         if not store:
#             return Response({'error': 'Store not configured'}, status=500)

#         # Determine customer (if logged in)
#         customer = None
#         if request.user and not isinstance(request.user, AnonymousUser):
#             try:
#                 customer = request.user.customer
#                 print("🧪 Authenticated user detected:", customer.email)  # Optional debug
#             except Exception as e:
#                 print("❌ Couldn't attach customer:", str(e))
#                 # pass

#         with transaction.atomic():
#             try:
#                 inventory = Inventory.objects.select_for_update().get(product=product, store=store)
#             except Inventory.DoesNotExist:
#                 return Response({"error": "Inventory not found."}, status=404)

#             if inventory.quantity < quantity:
#                 return Response({"error": "Not enough inventory."}, status=400)

#             inventory.quantity -= quantity
#             inventory.save()

#             # Create or get cart
#             if customer:
#                 cart = Carts.objects.filter(customer=customer, status='active').first()
#                 if not cart:
#                     cart = Carts.objects.create(
#                         customer=customer,
#                         status='active',
#                         total_qty=0,
#                         total_amount=Decimal('0.00'),
#                         # created_at=timezone.now(),
#                         # updated_at=timezone.now()
#                     )
#             else:
#                 session_key = request.session.session_key or request.session.create()
#                 guest_cart_id = request.session.get('guest_cart_id')

#                 cart = Carts.objects.filter(pk=guest_cart_id, customer=None, status='active').first() if guest_cart_id else None

#                 if not cart:
#                     cart = Carts.objects.create(
#                         customer=None,
#                         status='active',
#                         total_qty=0,
#                         total_amount=Decimal('0.00'),
#                         # created_at=timezone.now(),
#                         # updated_at=timezone.now()
#                     )
#                     request.session['guest_cart_id'] = cart.cart_id

#             # Add item to cart
#             cart_item, created = CartItems.objects.get_or_create(
#                 cart=cart,
#                 product=product,
#                 defaults={'quantity': quantity, 'price': product.price}
#             )

#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()

#             cart.total_qty = sum(item.quantity for item in cart.cartitems_set.all())
#             cart.total_amount = sum(item.quantity * item.price for item in cart.cartitems_set.all())
#             # cart.updated_at = timezone.now()
#             cart.save()

#         return Response({'message': 'Product added to cart'}, status=200)



# OLDEST


# class AddToCartView(APIView):
#     def post(self, request):
#         data = request.data
#         customer_id = data.get('customer_id')
#         product_id = data.get('product_id')
#         quantity = int(data.get('quantity', 1))

#         if not all([customer_id, product_id]):
#             return Response({'error': 'customer_id and product_id are required.'}, status=400)

#         try:
#             product = Products.objects.get(product_id=product_id)
#         except Products.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=404)

#         store = Stores.objects.first()
#         if not store:
#             return Response({'error': 'Store not configured'}, status=500)

#         with transaction.atomic():
#             try:
#                 inventory = Inventory.objects.select_for_update().get(product=product, store=store)
#             except Inventory.DoesNotExist:
#                 return Response({"error": "Inventory not found for this product."}, status=404)

#             if inventory.quantity < quantity:
#                 return Response({"error": "Not enough inventory."}, status=400)

#             # inventory.quantity -= quantity
#             # inventory.save()

#             cart = Carts.objects.filter(customer_id=customer_id, status='active').first()
#             if not cart:
#                 cart = Carts.objects.create(
#                     customer_id=customer_id,
#                     status='active',
#                     total_qty=0,
#                     total_amount=Decimal('0.00')
#                 )

#             cart_item, created = CartItems.objects.get_or_create(
#                 cart=cart,
#                 product=product,
#                 defaults={'quantity': quantity, 'price': product.price}
#             )
#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()

#             cart.total_qty = sum(item.quantity for item in cart.cartitems_set.all())
#             cart.total_amount = sum(item.quantity * item.price for item in cart.cartitems_set.all())
#             cart.save()

#         return Response({'message': 'Added to cart'}, status=200)







