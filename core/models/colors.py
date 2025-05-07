from django.db import models
from core.models.base import TimeStampedModel

class Colors(models.Model):
    color_id = models.BigAutoField(primary_key=True)
    color_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'colors'