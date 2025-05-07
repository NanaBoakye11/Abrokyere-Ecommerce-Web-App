from core.models.customers import Customers
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password



def create_customer(data):
    try:
        customer = Customers.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            phone=data.get('phone')
        ) 
        return customer
    except IntegrityError as e:
        raise ValueError('Email or phone already exists.')
    


def authenticate_customer(email, password):
    try:
        customer = Customers.objects.get(email=email)
        print("Found user:", customer.email)
        print("Stored hash:", customer.password)
        print("Match:", check_password(password, customer.password))
        if check_password(password, customer.password):
            return customer
        else:
            return None
    except Customers.DoesNotExist:
        return None