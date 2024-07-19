# users/urls.py
from django.urls import path

from .views import (SaleDetailView, SaleListAPIView, SalePriceUpdateAPIView,
                    SaleRegisterAPIView)

urlpatterns = [
    path("list", SaleListAPIView.as_view(), name="sale-list"),
    path("<int:pk>", SaleDetailView.as_view(), name="sale-detail"),
    path("register", SaleRegisterAPIView.as_view(), name="sale-register"),
    path(
        "change/<int:pk>",
        SalePriceUpdateAPIView.as_view(),
        name="sale-price-update",
    ),
]
