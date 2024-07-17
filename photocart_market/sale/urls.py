# users/urls.py
from django.urls import path

from .views import SaleDetailView, SaleListView

urlpatterns = [
    path("sale/list", SaleListView.as_view(), name="sale-list"),
    path("sale/<int:pk>", SaleDetailView.as_view(), name="sale-detail"),
]
