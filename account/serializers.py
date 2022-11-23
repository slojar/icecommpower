from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers

from account.models import Customer, Transaction
from icecommpower.exceptions import InvalidRequestException
from superadmin.utils import process_payment_with_card, generate_paystack_ref_no


class UserSignUpSerializerIn(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = username = validated_data.get('email').lower()
        password = validated_data.get('password')

        user, _ = User.objects.get_or_create(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    is_admin = serializers.BooleanField(write_only=True, required=False)
    email = serializers.CharField(source="user.email", read_only=True)
    last_login = serializers.CharField(source="user.last_login", read_only=True)

    class Meta:
        model = Customer
        exclude = ["user"]

    def update(self, instance, validated_data):
        user = validated_data.get('current_user')

        customer = super(CustomerSerializer, self).update(instance, validated_data)

        if validated_data.get('first_name'):
            customer.user.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            customer.user.last_name = validated_data.get('last_name')
        if validated_data.get('is_admin'):
            if not user.is_staff:
                raise InvalidRequestException({'detail': "You are not authorized to perform this action"})
            customer.user.is_staff = validated_data.get('is_admin')

        customer.user.save()
        return CustomerSerializer(customer, context=self.context).data


class SignUpSerializerIn(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(max_length=11, min_length=11)
    email = serializers.EmailField()
    gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField()

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        phone_no = validated_data.get('phone_number')
        email = validated_data.get('email').lower()
        gender = validated_data.get('gender')
        password = validated_data.get('password')

        # Check for email availability
        if User.objects.filter(email=email).exists():
            raise InvalidRequestException({"detail": "Email address is taken, please use another one"})

        # Create user instance
        user, _ = User.objects.get_or_create(username=email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()

        # Create customer
        customer, _ = Customer.objects.get_or_create(user=user)
        customer.phone_number = phone_no
        customer.gender = gender
        customer.save()

        data = CustomerSerializer(customer, context=self.context).data
        return data


class TransactionSerializerOut(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Transaction
        exclude = []


class TransactionSerializerIn(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('customer', 'payment_method', 'amount', 'description')

    def create(self, validated_data):
        # customer = validated_data.get('customer')
        payment_method = validated_data.get('payment_method')
        # amount = validated_data.get('amount')
        request = self.context.get('request')
        payment_link = None

        instance = super(TransactionSerializerIn, self).create(validated_data)

        # Create Transaction
        instance.reference = generate_paystack_ref_no(instance.id)
        instance.save()

        callback_url = request.build_absolute_uri(reverse('account:verify-transaction'))
        if payment_method == "card":
            success, payment_link = process_payment_with_card(transaction=instance, callback_url=callback_url)
            if not success:
                raise InvalidRequestException({'detail': payment_link})
        if payment_method == "wallet":
            ...

        data = {
            'detail': "Transaction created successfully",
            'payment_link': payment_link,
            'data': TransactionSerializerOut(instance=instance, context=self.context).data
        }
        return data

