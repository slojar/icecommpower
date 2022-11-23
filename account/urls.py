from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('signup/', views.SignUpAPIView.as_view(), name='sign-up'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('verify-transaction', views.VerifyTransactionAPIView.as_view(), name='verify-transaction'),

]

