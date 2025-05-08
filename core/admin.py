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



