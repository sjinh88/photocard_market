# users/urls.py
from django.urls import path

from .views import (BuyCancelAPIView, BuyEndAPIView, BuyListAPIView,
                    BuyRegisterAPIView)

urlpatterns = [
    path("register/<int:pk>", BuyRegisterAPIView.as_view(), name="photocard_buy"),
    path("cancel/<int:pk>", BuyCancelAPIView.as_view(), name="photocard_buy_cancel"),
    path("end/<int:pk>", BuyEndAPIView.as_view(), name="photocard_buy_end"),
    path("list", BuyListAPIView.as_view(), name="photocard_buy_list"),
]
