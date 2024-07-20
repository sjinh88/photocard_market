from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import PhotoCard
from .serializers import PhotoCardFilter, PhotoCardListSerializer


class PhotoCardListAPIView(generics.ListAPIView):
    """
    앱에 등록된 포토카드 리스트
    - 포토카드는 관리자 화면에서 등록을 함.
    - 관리자가 등록한 카드가 앱에 표시되며, 표시된 카드에 한하여 거래가 됨.
    """

    permission_classes = [AllowAny]
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardListSerializer


class PhotoCardSearchAPIView(generics.ListAPIView):
    """
    앱에 등록된 포토카드 검색
    """

    permission_classes = [AllowAny]
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PhotoCardFilter
