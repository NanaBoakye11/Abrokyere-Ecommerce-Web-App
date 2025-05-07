from django.db import models
from core.models.base import TimeStampedModel

class Customers(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=250)
    phone = models.CharField(unique=True, max_length=250)
   

    class Meta:
        managed = False
        db_table = 'customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"