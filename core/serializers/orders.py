# core/serializers/orders.py
from rest_framework import serializers
from core.models import Orders, OrderItems

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = OrderItems
        fields = ['order_item_id', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['order_id', 'order_date', 'total_amount', 'status', 'items']

    def get_items(self, obj):
        qs = OrderItems.objects.select_related('product').filter(order=obj)
        return OrderItemSerializer(qs, many=True).data
