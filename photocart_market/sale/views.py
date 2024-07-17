from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SaleHistory
from .serializers import SaleHistorySerializer


class SaleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer

    def get(self, request, *args, **kwargs):
        return Response([])


class SaleDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer

    def get(self, request, *args, **kwargs):
        return Response({})
