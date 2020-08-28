from django.urls import path

from .views import reset_password

urlpatterns = [
    path('reset-password/', reset_password),
]
