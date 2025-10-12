# core/models/stripe_sessions.py
from django.db import models

class StripeCheckoutSession(models.Model):
    stripe_session_id = models.CharField(max_length=255, unique=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, related_name='stripe_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stripe_checkout_sessions'
        managed = True

    def __str__(self):
        return f"{self.stripe_session_id} -> order {self.order_id}"
