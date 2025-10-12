# core/models/order_session_map.py
from django.db import models

class OrderSessionMap(models.Model):
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)

    class Meta:
        db_table = 'order_session_map'
        managed = True  # we create this table
