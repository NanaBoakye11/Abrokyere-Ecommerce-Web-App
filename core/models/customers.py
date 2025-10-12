from django.db import models
from core.models.base import TimeStampedModel
from django.contrib.auth.models import User


class Customers(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,  related_name='customer')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=250)
    phone = models.CharField(unique=True, max_length=250)
   

    class Meta:
        managed = False
        db_table = 'customers'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"