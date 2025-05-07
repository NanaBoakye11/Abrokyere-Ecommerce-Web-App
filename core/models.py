# {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'Abrokyere', 'USER': 'postgres', 'PASSWORD': 'OfatherAchimota2016!', 'HOST': 'localhost', 'PORT': '5432'}}
# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


# class Addresses(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     street_address = models.CharField(max_length=250, blank=True, null=True)
#     city = models.CharField(max_length=250, blank=True, null=True)
#     state = models.CharField(max_length=250, blank=True, null=True)
#     country = models.CharField(max_length=250, blank=True, null=True)
#     postal_code = models.CharField(max_length=250, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     cust = models.ForeignKey('Customers', models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'addresses'


# class CartItems(models.Model):
#     cart_item_id = models.AutoField(primary_key=True)
#     cart = models.ForeignKey('Carts', models.DO_NOTHING)
#     product = models.ForeignKey('Products', models.DO_NOTHING)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=15, decimal_places=2)

#     class Meta:
#         managed = False
#         db_table = 'cart_items'


# class Carts(models.Model):
#     cart_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey('Customers', models.DO_NOTHING)
#     total_qty = models.IntegerField(blank=True, null=True)
#     total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'carts'


# class Categories(models.Model):
#     category_id = models.AutoField(primary_key=True)
#     category_name = models.CharField(max_length=50)
#     sub_cat_name = models.CharField(max_length=50, blank=True, null=True)
#     sub_sub_cat_name = models.CharField(max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'categories'


# class Clerks(models.Model):
#     clerk_id = models.AutoField(primary_key=True)
#     employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'clerks'


# class Colors(models.Model):
#     color_id = models.AutoField(primary_key=True)
#     color_name = models.CharField(unique=True, max_length=50)

#     class Meta:
#         managed = False
#         db_table = 'colors'


# class Customers(models.Model):
#     cust_id = models.AutoField(primary_key=True)
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     email = models.CharField(unique=True, max_length=100)
#     password = models.CharField(max_length=250)
#     phone = models.CharField(unique=True, max_length=250)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'customers'


# class Deliveries(models.Model):
#     delivery_id = models.AutoField(primary_key=True)
#     delivery_address = models.CharField(max_length=255)
#     driver = models.ForeignKey('Drivers', models.DO_NOTHING)
#     order = models.ForeignKey('Orders', models.DO_NOTHING)
#     delivery_method = models.TextField()  # This field type is a guess.
#     delivery_status = models.TextField(blank=True, null=True)  # This field type is a guess.
#     scheduled_delievery_time = models.DateTimeField(blank=True, null=True)
#     actual_dt = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     instructions = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'deliveries'


# class Drivers(models.Model):
#     driver_id = models.AutoField(primary_key=True)
#     employee = models.OneToOneField('Employees', models.DO_NOTHING)
#     driver_license = models.CharField(unique=True, max_length=50)
#     license_country = models.CharField(max_length=200)
#     vehicle_type = models.TextField()  # This field type is a guess.
#     plate_number = models.CharField(max_length=50, blank=True, null=True)
#     num_of_deliveries = models.IntegerField(blank=True, null=True)
#     profile_pic = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'drivers'


# class Employees(models.Model):
#     employee_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50, blank=True, null=True)
#     last_name = models.CharField(max_length=50)
#     email = models.CharField(unique=True, max_length=100)
#     phone = models.CharField(unique=True, max_length=200)
#     birthday = models.DateField(blank=True, null=True)
#     role = models.ForeignKey('Roles', models.DO_NOTHING)
#     start_date = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'employees'


# class Inventory(models.Model):
#     inventory_id = models.AutoField(primary_key=True)
#     store = models.ForeignKey('Stores', models.DO_NOTHING)
#     product = models.ForeignKey('Products', models.DO_NOTHING)
#     color = models.ForeignKey(Colors, models.DO_NOTHING)
#     quantity = models.IntegerField(blank=True, null=True)
#     category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
#     location = models.CharField(max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'inventory'


# class OrderItems(models.Model):
#     order_item_id = models.AutoField(primary_key=True)
#     order = models.ForeignKey('Orders', models.DO_NOTHING)
#     product = models.ForeignKey('Products', models.DO_NOTHING)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=15, decimal_places=2)

#     class Meta:
#         managed = False
#         db_table = 'order_items'


# class Orders(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(Customers, models.DO_NOTHING)
#     order_date = models.DateTimeField(blank=True, null=True)
#     total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
#     status = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = 'orders'


# class Permissions(models.Model):
#     permission_id = models.AutoField(primary_key=True)
#     permission_name = models.CharField(max_length=50)
#     level_number = models.IntegerField()
#     description = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'permissions'


# class Products(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
#     product_name = models.CharField(max_length=500)
#     price = models.DecimalField(max_digits=15, decimal_places=2)
#     description = models.CharField(max_length=500, blank=True, null=True)
#     prod_reviews = models.CharField(max_length=600, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'products'


# class Roles(models.Model):
#     role_id = models.AutoField(primary_key=True)
#     role_name = models.CharField(unique=True, max_length=50)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     permission = models.ForeignKey(Permissions, models.DO_NOTHING, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'roles'


# class Sellers(models.Model):
#     seller_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.CharField(unique=True, max_length=100)
#     phone = models.CharField(unique=True, max_length=200)
#     password = models.CharField(max_length=255)
#     sex = models.TextField(blank=True, null=True)  # This field type is a guess.
#     seller_add = models.ForeignKey('SellersAddresses', models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'sellers'


# class SellersAddresses(models.Model):
#     seller_add_id = models.AutoField(primary_key=True)
#     street_address = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     country = models.CharField(max_length=200)

#     class Meta:
#         managed = False
#         db_table = 'sellers_addresses'


# class Stores(models.Model):
#     store_id = models.AutoField(primary_key=True)
#     seller = models.ForeignKey(Sellers, models.DO_NOTHING)
#     store_name = models.CharField(unique=True, max_length=100)
#     country = models.CharField(max_length=50, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     postal_code = models.CharField(max_length=50, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     store_logo = models.CharField(max_length=255, blank=True, null=True)
#     payment_info = models.CharField(max_length=255, blank=True, null=True)
#     website_url = models.CharField(max_length=255, blank=True, null=True)
#     reviews = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'stores'


# class Verifications(models.Model):
#     verification_id = models.AutoField(primary_key=True)
#     sellers = models.ForeignKey(Sellers, models.DO_NOTHING, blank=True, null=True)
#     government_id = models.CharField(unique=True, max_length=200)
#     country_issued_id = models.CharField(max_length=200)
#     business_name = models.CharField(unique=True, max_length=200)
#     business_regis_num = models.CharField(unique=True, max_length=200)
#     bank_name = models.CharField(max_length=200)
#     bank_account_number = models.CharField(unique=True, max_length=100)
#     routing_number = models.CharField(max_length=100)
#     status = models.TextField(blank=True, null=True)  # This field type is a guess.
#     submitted_at = models.DateTimeField()
#     updated_at = models.DateTimeField(blank=True, null=True)
#     verified_by = models.ForeignKey(Employees, models.DO_NOTHING, db_column='verified_by', blank=True, null=True)
#     decision_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'verifications'
