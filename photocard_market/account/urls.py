# users/urls.py
from django.urls import path

from .views import LoginAPIView, RegisterAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="user_signup"),
    path("login/", LoginAPIView.as_view(), name="user_login"),
]
