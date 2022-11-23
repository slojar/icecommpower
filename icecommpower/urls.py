from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("account.urls")),
    path('superadmin/', include("superadmin.urls")),
    path('admin/', admin.site.urls),
]

