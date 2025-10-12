from django.contrib import admin
from core.models import (Customers, Orders, Products, CustomerAddresses, CartItems, Carts, Categories, Clerks, Colors, Deliveries, Drivers, Employees, Inventory, OrderItems, Permissions, Roles, Sellers, SellersAddresses, Stores, Verifications, ProductImages, SubCategories, ProductReviews, OrderSessionMap) # Add more as needed
from core.models import WebhookEventLog


admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(CustomerAddresses)
admin.site.register(Colors)
admin.site.register(CartItems)
admin.site.register(Employees)
admin.site.register(Drivers)
admin.site.register(Deliveries)
admin.site.register(Carts)
admin.site.register(Categories)
admin.site.register(Clerks)
admin.site.register(Inventory)
admin.site.register(OrderItems)
admin.site.register(Permissions)
admin.site.register(Roles)
admin.site.register(Sellers)
admin.site.register(SellersAddresses)
admin.site.register(Stores)
admin.site.register(Verifications)
admin.site.register(ProductImages)
admin.site.register(SubCategories)
admin.site.register(ProductReviews)
admin.site.register(OrderSessionMap)

# @admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer", "status", "total_amount", "order_date")
    search_fields = ("order_id", "customer__email")

# @admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("order_item_id", "order", "product", "quantity", "price")

@admin.register(WebhookEventLog)
class WebhookEventLogAdmin(admin.ModelAdmin):
    list_display = ("event_id", "created_at")
    search_fields = ("event_id",)
