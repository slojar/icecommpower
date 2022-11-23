import django_heroku
from .base import *


SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ["*", "payarenamall.tm-dev.xyz"]

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated']
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', 'Token',),
}


PAYSTACK_BASE_URL = env('PAYSTACK_BASE_URL')
PAYSTACK_SECRET_KEY = env('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env('PAYSTACK_PUBLIC_KEY')
PAYSTACK_REF = env('PAYSTACK_REF')


# Activate Django-Heroku.
django_heroku.settings(locals())



