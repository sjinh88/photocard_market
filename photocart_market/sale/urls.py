# users/urls.py
from django.urls import path

from .views import (SaleDetailView, SaleListAPIView, SalePriceUpdateAPIView,
                    SaleRegisterAPIView)

urlpatterns = [
    path("sale/list", SaleListAPIView.as_view(), name="sale-list"),
    path("sale/<int:pk>", SaleDetailView.as_view(), name="sale-detail"),
    path("sale/register", SaleRegisterAPIView.as_view(), name="sale-register"),
    path(
        "sale/change/<int:pk>",
        SalePriceUpdateAPIView.as_view(),
        name="sale-price-update",
    ),
]
