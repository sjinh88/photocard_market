# users/urls.py
from django.urls import path

from .views import (SaleDetailView, SaleListAPIView, SalePriceUpdateAPIView,
                    SaleRegisterAPIView)

urlpatterns = [
    path("list", SaleListAPIView.as_view(), name="sale_list"),
    path("<int:pk>", SaleDetailView.as_view(), name="sale_detail"),
    path("register", SaleRegisterAPIView.as_view(), name="sale_register"),
    path(
        "change/<int:pk>",
        SalePriceUpdateAPIView.as_view(),
        name="sale_price_update",
    ),
]
