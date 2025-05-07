from django.contrib import admin
from core.models import (Customers, Orders, Products, CustomerAddresses, CartItems, Carts, Categories, Clerks, Colors, Deliveries, Drivers, Employees, Inventory, OrderItems, Permissions, Roles, Sellers, SellersAddresses, Stores, Verifications, ProductImages, SubCategories) # Add more as needed


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











# A reusable base admin config for timestamped models


























# models = [
# Customers, Orders, Products, CustomerAddresses, CartItems, Carts, Categories, 
# Clerks, Colors, Deliveries, Drivers, Employees, Inventory, OrderItems, 
# Permissions, Roles, Sellers, SellersAddresses, Stores, Verifications
# ]


# # Register models here.

# for model in models:
#     admin.site.register(model)

# class TimestampedAdmin(admin.ModelAdmin):
#     readonly_fields = ('created_at', 'updated_at')
#     ordering = ('-created_at',)


# @admin.register(Customers)
# class CustomersAdmin(TimestampedAdmin):
#     list_display = ('customer_id', 'first_name', 'last_name', 'email', 'phone')


# @admin.register(CustomerAddresses)
# class CustomerAddressesAdmin(TimestampedAdmin):
#     list_display = ('address_id', 'customer', 'city', 'state')


# @admin.register(Orders)
# class OrdersAdmin(TimestampedAdmin):
#     list_display = ('order_id', 'customer_id', 'order_date', 'status')


# @admin.register(Products)
# class ProductsAdmin(TimestampedAdmin):
#     list_display = ('product_id', 'product_name', 'price', 'category_id')


# @admin.register(Carts)
# class CartsAdmin(TimestampedAdmin):
#     list_display = ('cart_id', 'customer_id', 'total_qty', 'total_amount')


# @admin.register(Deliveries)
# class DeliveriesAdmin(TimestampedAdmin):
#     list_display = ('delivery_id', 'order_id', 'delivery_method', 'delivery_status')


# @admin.register(Employees)
# class EmployeesAdmin(TimestampedAdmin):
#     list_display = ('employee_id', 'first_name', 'last_name', 'email', 'role_id')


# @admin.register(Sellers)
# class SellersAdmin(TimestampedAdmin):
#     list_display = ('seller_id', 'first_name', 'last_name', 'email', 'phone')


# @admin.register(Stores)
# class StoresAdmin(TimestampedAdmin):
#     list_display = ('store_id', 'store_name', 'seller_id', 'city', 'country')


# # For simple tables that don't need customization:
# admin.site.register(CartItems)
# admin.site.register(OrderItems)
# admin.site.register(Colors)
# admin.site.register(Categories)
# admin.site.register(Clerks)
# admin.site.register(Drivers)
# admin.site.register(Inventory)
# admin.site.register(Permissions)
# admin.site.register(Roles)
# admin.site.register(SellersAddresses)
# admin.site.register(Verifications)