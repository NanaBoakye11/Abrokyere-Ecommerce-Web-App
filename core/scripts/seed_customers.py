from core.models import Customers
from django.utils.crypto import get_random_string

def run():
    for i in range(100):
        Customers.objects.create(
            first_name=f'Test{i}',
            last_name=f'User{i}',
            email=f'testuser{i}@example.com',
            phone=f'555000{i:04}',
            password='Test@1234' 
        )