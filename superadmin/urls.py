from django.urls import path
from . import views


urlpatterns = [
    path('customer/', views.CustomerListCreateAPIView.as_view(), name='customer'),
    path('customer/<int:id>/', views.CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-detail'),
    path('customer/<int:id>/transactions/', views.CustomerTransactionView.as_view(), name='customer-transactions'),
    path('transactions/', views.CustomerTransactionView.as_view(), name='transaction'),
    path('transactions/<int:id>/', views.TransactionAPIView.as_view(), name='transaction-detail'),

]

