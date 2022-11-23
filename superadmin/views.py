from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser

from django.contrib.auth.models import User

from account.models import Customer, Transaction
from account.paginations import CustomPagination
from account.serializers import CustomerSerializer, TransactionSerializerOut, TransactionSerializerIn
from icecommpower.exceptions import raise_serializer_error_msg


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('-created_on')

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        phone_no = data.get("phone_number")
        gender = data.get("gender")

        is_admin = data.get("is_admin", False)
        verified = data.get("verified", False)

        # Check if User with email already exist
        if User.objects.filter(email=email).exists():
            return Response({"detail": "A user with this email already exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create user
            user, created = User.objects.get_or_create(email=email)
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.is_staff = is_admin
            user.save()

            # Create customer
            customer, created = Customer.objects.get_or_create(user=user)
            customer.gender = gender
            if phone_no:
                # Reformat phone number
                phone_number = f"0{phone_no[-10:]}"
                customer.phone_number = phone_number
            customer.verified = verified
            customer.save()
            return Response({"detail": "Account created successfully", "data": CustomerSerializer(customer, context=self.get_serializer_context()).data})
        except Exception as err:
            return Response({"detail": "An error has occurred", "error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Customer.objects.all().order_by("-created_on")
    serializer_class = CustomerSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('id')
        customer = get_object_or_404(Customer, id=customer_id, active=True)
        serializer = CustomerSerializer(instance=customer, data=request.data, context=self.get_serializer_context())
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        result = serializer.save()

        data = dict()
        data['detail'] = "Customer updated successfully"
        data['data'] = result
        return Response(data)

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('id')
        customer = get_object_or_404(Customer, id=customer_id, active=True)
        customer.active = False
        customer.save()
        # customer.delete()
        # The customer active is set to False, instead of deleting the customer instance.
        return Response({"detail": "Account deleted successfully"})


class CustomerTransactionView(generics.ListCreateAPIView):
    pagination_class = CustomPagination
    queryset = Transaction.objects.filter(active=True)
    serializer_class = TransactionSerializerOut
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        customer_id = self.kwargs.get('id')
        if customer_id:
            customer = get_object_or_404(Customer, id=customer_id, active=True)
            return customer.transaction_set.filter(active=True)
        return Transaction.objects.filter(active=True)

    def post(self, request, **kwargs):
        serializer = TransactionSerializerIn(data=request.data, context=self.get_serializer_context())
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data = serializer.save()
        return Response(data)


class TransactionAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Transaction.objects.filter(active=True)
    permission_classes = (IsAdminUser,)
    serializer_class = TransactionSerializerOut




