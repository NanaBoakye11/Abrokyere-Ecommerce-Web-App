from django.db import models
from core.models.base import TimeStampedModel

class Categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)


    class Meta:
        managed = False
        db_table = 'categories'