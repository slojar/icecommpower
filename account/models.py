from django.db import models
from django.contrib.auth.models import User
from .choices import GENDER_CHOICES, PAYMENT_METHOD_CHOICES, PAYMENT_STATUS_CHOICES


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default="male")
    profile_picture = models.ImageField(upload_to='profile-pictures', null=True, blank=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"{self.user.first_name}-{self.user.last_name}"


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default="card")
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.id} - {self.amount}: {self.status}"

