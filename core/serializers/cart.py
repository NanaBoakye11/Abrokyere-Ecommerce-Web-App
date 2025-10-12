# core/serializers/cart.py
from rest_framework import serializers
from core.models import Carts, CartItems, Products, ProductImages

# This serializer is used to *receive* data when adding/updating items to the cart
class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField() # Expects product_id from frontend
    quantity = serializers.IntegerField(min_value=1) # Expects quantity, must be at least 1

# This serializer is used to *send back* cart item details as part of the CartSerializer response
class CartItemResponseSerializer(serializers.ModelSerializer):
    # Use source to get product name from related Product model
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=15, decimal_places=2, read_only=True)
    # Method field to get the main image URL for the product
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        # Fields to include in the response for each cart item
        fields = ['cart_item_id', 'product', 'product_name', 'product_price', 'quantity', 'price', 'image_url']
        # 'product' and 'price' are typically read-only as they are derived/set by the backend
        read_only_fields = ['product', 'price']

    def get_image_url(self, obj):
        # Assuming your Product model has a related_name (e.g., 'product_images') to ProductImages
        # and ProductImages has an 'is_main' field.
        main_image = obj.product.product_images.filter(is_main=True).first()
        if main_image:

            request = self.context.get('request')
            return request.build_absolute_uri(main_image.image_url)
            # return main_image.image_url
        return None # Return None or a default image URL if no main image

# This serializer is used to *send back* the entire cart details, including nested items
class CartSerializer(serializers.ModelSerializer):
    # Nested serializer to display cart items
    cart_items = CartItemResponseSerializer(many=True, read_only=True)
    # Display customer_id if a customer is linked
    customer_id = serializers.IntegerField(source='customer.customer_id', read_only=True)

    class Meta:
        model = Carts
        # Fields to include in the cart response
        fields = ['cart_id', 'customer_id', 'total_qty', 'total_amount', 'status', 'cart_items']