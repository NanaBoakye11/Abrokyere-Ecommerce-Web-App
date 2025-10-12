from core.models.customers import Customers
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User # <-- Import Django's User model
from django.contrib.auth import authenticate #


def create_customer(data):
    # Use a database transaction to ensure atomicity
    # If User creation fails, Customers creation will also be rolled back
    with transaction.atomic():
        try:
            # 1. Create Django User
            # We use set_password for User model, which handles hashing
            user = User.objects.create_user(
                username=data.get('email'), # Often use email as username for login
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name', ''), # Django User also has first/last name
                last_name=data.get('last_name', '')
            )
            # user.set_password(data.get('password')) # create_user already does this
            # user.save()

            # 2. Create Customers profile linked to the new User
            customer = Customers.objects.create(
                user=user, # Link to the new User instance
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=make_password(data.get('password')), # Keep for your Customers model if you still want it
                phone=data.get('phone')
            )
            return customer
        except IntegrityError as e:
            # Catch duplicate email/username from User model or Customers model
            if 'username' in str(e) or 'email' in str(e): # Check for Django User related errors
                raise ValueError('Email already exists.')
            if 'phone' in str(e): # Check for your Customers model phone error
                raise ValueError('Phone number already exists.')
            raise ValueError(f'Registration failed: {e}') # General error

def authenticate_customer(email, password):
    # 1. Authenticate using Django's built-in authentication system
    user = authenticate(username=email, password=password)

    if user is not None:
        # User is authenticated. Now get the linked Customers profile.
        try:
            # Use the 'user' field in your Customers model
            customer = Customers.objects.get(user=user)
            print("Found user and linked customer:", customer.email)
            return customer
        except Customers.DoesNotExist:
            # This should ideally not happen if create_customer always creates a linked profile
            print("ERROR: Authenticated user found, but no linked Customers profile.")
            return None # Or raise an error as this indicates an inconsistency
    else:
        print("Authentication failed for email:", email)
        return None



# def create_customer(data):
#     try:
#         customer = Customers.objects.create(
#             first_name=data.get('first_name'),
#             last_name=data.get('last_name'),
#             email=data.get('email'),
#             password=make_password(data.get('password')),
#             phone=data.get('phone')
#         ) 
#         return customer
#     except IntegrityError as e:
#         raise ValueError('Email or phone already exists.')
    


# def authenticate_customer(email, password):
#     try:
#         customer = Customers.objects.get(email=email)
#         print("Found user:", customer.email)
#         # print("Stored hash:", customer.password)
#         print("Match:", check_password(password, customer.password))
#         if check_password(password, customer.password):
#             return customer
#         else:
#             return None
#     except Customers.DoesNotExist:
#         return None