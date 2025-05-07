# core/views/auth.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from core.serializers.customers import CustomerRegisterSerializer
from core.services.customer_service import create_customer
from core.serializers.auth import CustomerLoginSerializer
from core.services.customer_service import authenticate_customer
from core.serializers.customers import CustomerRegisterSerializer, CustomerResponseSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = create_customer(serializer.validated_data)
                response_data = CustomerResponseSerializer(customer).data
                return Response({
                    "message": "Customer registered successfully",
                    "customer": response_data
                    }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            customer = authenticate_customer(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            if customer:
                return Response({"message": "Login successful", "customer_id": customer.customer_id})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)