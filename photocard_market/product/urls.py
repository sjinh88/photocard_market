# users/urls.py
from django.urls import path

from .views import PhotoCardListAPIView, PhotoCardSearchAPIView

urlpatterns = [
    path("photocard/list", PhotoCardListAPIView.as_view(), name="photocard-list"),
    path("photocard/search", PhotoCardSearchAPIView.as_view(), name="photocard-search"),
]
