from django.conf import settings
from django.db.models import F, Q
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .enums import State
from .models import SaleHistory
from .serializers import (
    SaleDetailSerializer,
    SaleHistorySerializer,
    SalePriceUpdateSerializer,
    SaleResigterSerializer,
)
from .utils import fee_calculate


class SaleRegisterAPIView(generics.CreateAPIView):
    """
    판매할 카드 등록
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SaleResigterSerializer

    @swagger_auto_schema(tags=["photocard/sale"])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(
                seller=request.user, fee=fee_calculate(request.data["price"])
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalePriceUpdateAPIView(generics.UpdateAPIView):
    """
    판매 가격 변경
    - 변경을 요청한 카드가 요청자가 생성한 카드인지 확인함
    - 거래중 / 판매완료 상태일 때는 변경 불가
    """

    permission_classes = [IsAuthenticated]
    queryset = SaleHistory.objects.all()
    serializer_class = SalePriceUpdateSerializer

    @swagger_auto_schema(tags=["photocard/sale"])
    def put(self, request, *args, **kwargs):
        # pk(photo_card_id)를 가격 수정을 요청한 사람이 등록했는지 확인
        instance = get_object_or_404(
            self.queryset, id=kwargs["pk"], seller_id=request.user.id
        )
        # 판매완료 / 판매중(거래중) -> 가격 변경 불가
        if instance.state in [State.END, State.BEGIN]:
            return Response(
                data={
                    "message": "판매중이거나 판매완료된 상태는 가격 변경이 되지 않습니다."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 판매 등록
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            fee=fee_calculate(request.data["price"]),
            renewal_date=timezone.now(),
        )
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        # patch 요청은 사용 안함.
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SaleListAPIView(generics.ListAPIView):
    """
    판매 리스트에 등록된 포토카드 리스트
    - 회원가입 or 로그인 되어 있지 않아도 조회는 가능
    """

    permission_classes = [AllowAny]
    queryset = SaleHistory.objects.all()
    serializer_class = SaleHistorySerializer

    @swagger_auto_schema(tags=["photocard/sale"])
    def get(self, request, *args, **kwargs):
        """
        현재 판매 가능한 포토카드 리스트 가져오기
        조건 :
          1. 현재 등록(S)인 건만 List에서 조회
          2. photo_card_id는 중복 O,
              2-1. 만약 동일한 photo_card_id -> 금액이 가장 낮은 걸로 조회.
              2-2. 최소 가격까지 모두 동일 -> renewal_date(가격 수정일)가 가장 먼저 등록걸로 조회
        """
        qs = (
            self.get_queryset()
            .filter(state=State.START)
            .annotate(
                rnk=Window(
                    expression=RowNumber(),
                    partition_by=[F("photo_card_id"), F("price")],
                    order_by=[F("photo_card_id"), F("price"), F("renewal_date")],
                )
            )
            .filter(Q(rnk=1))
        )
        qs = self.filter_queryset(qs)

        # pagenation 처리
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleDetailView(generics.RetrieveAPIView):
    """
    카드의 상세 정보
    """

    permission_classes = [AllowAny]
    queryset = SaleHistory.objects.all()
    serializer_class = SaleDetailSerializer

    @swagger_auto_schema(tags=["photocard/sale"])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # 총 판매 가격
        instance.total_price = instance.price + instance.fee
        # 조회된 포토카드 id의 최근(5개) 판매완료 내역 - 조회한 id는 제외
        instance.sale_history = (
            SaleHistory.objects.filter(
                state=State.END, photo_card_id=instance.photo_card_id
            )
            .exclude(id=kwargs["pk"])
            .order_by("-sold_date")
        )[: settings.SALE_LIST_LIMIT]
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
