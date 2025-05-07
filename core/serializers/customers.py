# core/serializers/customers.py
from core.models.customers import Customers
from rest_framework import serializers

class CustomerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    def validate_email(self, value):
        from core.models.customers import Customers
        if Customers.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class CustomerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['customer_id', 'first_name', 'last_name', 'email', 'phone']