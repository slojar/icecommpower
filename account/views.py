from django.contrib.auth import authenticate
from django.shortcuts import HttpResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import CustomerSerializer, TransactionSerializerOut, SignUpSerializerIn
from account.utils import perform_payment_verification
from icecommpower.exceptions import raise_serializer_error_msg


class HomeView(APIView):
    permission_classes = []

    def get(self, request):
        return HttpResponse("<h4>Welcome to ICECOMMPOWER BACKEND PORTAL</h4>")


class SignUpAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SignUpSerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        result = serializer.save()
        return Response({"detail": "Registration was successful", "data": result})


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([email, password]):
            return Response({"detail": "All fields are required: email and password"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=email, password=password)

        # Check if user exists
        if not user:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        # Update last login
        user.last_login = timezone.now()
        user.save()

        return Response({'detail': 'Login successful', 'token': f"{RefreshToken.for_user(user).access_token}",
                         'data': CustomerSerializer(user.customer, context={"request": request}).data})


class VerifyTransactionAPIView(APIView):
    permission_classes = []

    def get(self, request):
        ref = request.GET.get("reference")
        # Verify transaction
        success, transaction = perform_payment_verification(ref)
        if success is False:
            return Response({"detail": "Error occurred while validating transaction"})
        serializer = TransactionSerializerOut(transaction).data
        return Response({"detail": serializer})













