from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import PhotoCard
from .serializers import PhotoCardListSerializer


class PhotoCardListAPIView(generics.ListAPIView):
    """
    앱에서 거래가 가능한 포토카드 리스트
    - 포토카드는 관리자 화면에서 등록을 함.
    - 관리자가 등록한 카드가 앱에 표시되며, 표시된 카드에 한하여 거래가 됨.
    """
    permission_classes = [IsAdminUser]
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardListSerializer
