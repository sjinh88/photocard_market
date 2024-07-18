# users/urls.py
from django.urls import path

from .views import PhotoCardListAPIView

urlpatterns = [
    path("photocard/list/", PhotoCardListAPIView.as_view(), name="photocard-list"),
]
