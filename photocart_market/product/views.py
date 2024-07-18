from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import PhotoCard
from .serializers import PhotoCardListSerializer


class PhotoCardListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardListSerializer
