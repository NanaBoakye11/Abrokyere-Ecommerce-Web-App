# core/views/auth.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from core.models import Customers  
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from core.serializers.customers import CustomerRegisterSerializer
from core.services.customer_service import create_customer, authenticate_customer
from core.serializers.auth import CustomerLoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication # Add this
from core.serializers.customers import CustomerRegisterSerializer, CustomerResponseSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = create_customer(serializer.validated_data)
                # response_data = CustomerResponseSerializer(customer).data
                # return Response({
                #     "message": "Customer registered successfully",
                #     "customer": response_data
                #     }, status=status.HTTP_201_CREATED)

                return Response(CustomerResponseSerializer(customer).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]  # No authentication needed to login

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            customer = authenticate_customer(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            if customer:
                if not customer.user:
                    return Response({
                        "detail": "Customer account not fully set up. Please contact support."
                    }, status=status.HTTP_401_UNAUTHORIZED)

                # ✅ FIX: Pass `customer.user` (Django User model) to token generators
                access_token = AccessToken.for_user(customer.user)
                refresh_token = RefreshToken.for_user(customer.user)

                # ✅ Send customer info from linked Customers model
                customer_data = CustomerResponseSerializer(customer).data

                return Response({
                    "token": str(access_token),
                    "refresh": str(refresh_token),
                    "customer": customer_data
                }, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     permission_classes = [AllowAny] # No authentication needed to login

#     def post(self, request):
#         serializer = CustomerLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             customer = authenticate_customer(
#                 serializer.validated_data['email'],
#                 serializer.validated_data['password']
#             )
#             if customer:

#                 if customer.user is None:
#                     # This case should ideally not happen if all customers are linked to users.
#                     # Handle if a legacy customer without a linked User tries to log in.
#                     # You might need to link them here or disallow login.
#                     return Response({"detail": "Customer account not fully set up. Please contact support."}, status=status.HTTP_401_UNAUTHORIZED)
#                 # ✅ Explicitly create AccessToken and RefreshToken for the customer_id
#                 # This ensures the 'customer_id' claim is properly set in the token
#                 access_token = AccessToken.for_user(customer) # Pass your customer instance directly
#                 # Simple JWT will use USER_ID_FIELD='customer_id' as configured in settings
#                 refresh_token = RefreshToken.for_user(customer)


#                 customer_data = CustomerResponseSerializer(customer).data

#                 return Response({
#                     "token": str(access_token),
#                     "refresh": str(refresh_token), # Return refresh token too for token refreshing
#                     "customer": customer_data
#                 }, status=status.HTTP_200_OK)

#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthStatusView(APIView):
    authentication_classes = [JWTAuthentication] # This ensures JWT is processed
    permission_classes = [AllowAny] # Allow non-authenticated access, so we can check if logged in

    def get(self, request):
        if request.user.is_authenticated:
            print(f"DEBUG AuthStatus: request.user object: {request.user}")
            print(f"DEBUG AuthStatus: request.user.id (should be customer_id): {request.user.id}")
            try:
                # request.user will be a Simple JWT 'TokenUser' or similar object,
                # but its 'id' attribute should now be the customer_id due to USER_ID_FIELD setting.
                # Use request.user.id to get the customer_id
                # customer_id_from_token = request.user.id
                # customer = Customers.objects.get(customer_id=customer_id_from_token)
                customer = Customers.objects.get(user=request.user)

                # print(f"DEBUG AuthStatus: Found Customers instance for ID {customer_id_from_token}: {customer.email}")

                return Response({
                    "logged_in": True,
                    "email": customer.email,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "customer_id": customer.customer_id,
                })
            except Customers.DoesNotExist:
                return Response({"logged_in": False, "error": "Customer profile not found for token."}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e: # Catch other potential errors during token processing
                return Response({"logged_in": False, "error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response({"logged_in": False})




















# class LoginView(APIView):
#     def post(self, request):
#         serializer = CustomerLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             customer = authenticate_customer(
#                 serializer.validated_data['email'],
#                 serializer.validated_data['password']
#             )
#             if customer:
#                 # ✅ Generate JWT token for the authenticated customer
#                 refresh = RefreshToken.for_user(customer)
#                 access_token = str(refresh.access_token)

#                 customer_data = CustomerResponseSerializer(customer).data

#                 return Response({
#                     "token": access_token,
#                     "customer": customer_data
#                 }, status=status.HTTP_200_OK)

#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





























# class LoginView(APIView):
#     def post(self, request):
#         serializer = CustomerLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             customer = authenticate(request, email=email, password=password)
#             if customer:
#                 login(request, customer)  # ⬅️ Sets session cookie
#                 customer_data = CustomerResponseSerializer(customer).data
#                 return Response({
#                     "message": "Login successful",
#                     "customer": customer_data
#                 })
#             return Response({"detail": "Invalid credentials"}, status=401)

#         return Response(serializer.errors, status=400)
        

# class AuthStatusView(APIView):
#     def get(self, request):
#         if request.user and not isinstance(request.user, AnonymousUser):
#             try:
#                 customer = request.user.customer
#                 return Response({
#                     "logged_in": True,
#                     "email": customer.email,
#                     "first_name": customer.first_name,
#                     "last_name": customer.last_name,
#                     "customer_id": customer.customer_id,
#                 })
#             except Exception as e:
#                 return Response({"logged_in": False, "error": str(e)}, status=403)
#         return Response({"logged_in": False})