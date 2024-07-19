from account.models import UserWallet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sale.enums import State
from sale.models import SaleHistory

from .serializers import BuyListSerializer, BuyRequestSerializer


class BuyRegisterAPIView(generics.UpdateAPIView):
    """
    구매 등록
    - 구매요청한 사람 != 판매자
    - 구매 가격이 wallet에 있는 cash 보다 낮아야 구매 가능
    """

    serializer_class = BuyRequestSerializer
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["photocard/buy"])
    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs["pk"])
        # 판매 상태 체크
        if instance.seller.id == request.user.id:
            return Response(
                data={"message": "판매자와 구매자가 같습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # E: 판매완료 / B : 판매중(거래중) -> 거래 요청 불가
        if instance.state in [State.END, State.BEGIN]:
            return Response(
                data={"message": "판매중이거나 판매완료된 상태입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # wallet 정보 체크
        uw_instance = UserWallet.objects.get(user_id=request.user.id)
        if uw_instance.cash < (instance.price + instance.fee):
            return Response(
                data={"message": "보유한 cash가 부족합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 거래 등록
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(state=State.BEGIN, buyer=request.user)
        # wallet 금액 반영
        uw_instance.cash -= instance.price + instance.fee
        uw_instance.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BuyCancelAPIView(generics.UpdateAPIView):
    """
    구매 취소
    - 구매 취소한 사람 != 판매자
    - 판매 중(거래중) 상태만 구매 취소 가능
    """

    serializer_class = BuyRequestSerializer
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["photocard/buy"])
    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs["pk"])
        # 거래 상태 체크
        #   - 판매자 != 구매자인가??
        #   - 취소가 가능한 상태인가??
        #   - 이미 판매가 완료된 상태인가??
        if instance.seller.id == request.user.id:
            return Response(
                data={"message": "판매자와 구매자가 같습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.state in [State.START, State.END]:
            return Response(
                data={"message": "취소 가능한 상태가 아닙니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 거래 취소
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(state=State.START, buyer=None)

        # wallet 복원하기
        uw_instance = UserWallet.objects.get(user_id=request.user.id)
        uw_instance.cash += instance.price + instance.fee
        uw_instance.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BuyEndAPIView(generics.UpdateAPIView):
    """
    구매 완료
    - 구매 취소한 사람 != 판매자
    - 판매 중(거래중) 상태만 구매 완료 넘길 수 있음
    """

    serializer_class = BuyRequestSerializer
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["photocard/buy"])
    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs["pk"])
        # 거래 상태 체크
        #   - 판매자 != 구매자인가??
        #   - 거래 중 상태인가??
        #   - 이미 판매가 완료된 상태인가??
        if instance.seller.id == request.user.id:
            return Response(
                data={"message": "판매자와 구매자가 같습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.state in [State.START, State.END]:
            return Response(
                data={"message": "판매 중인 상태가 아닙니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 거래 완료
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            state=State.END,
            buyer=request.user,
            sold_date=timezone.now(),
        )

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BuyListAPIView(generics.ListAPIView):
    """
    구매 리스트
    - 현재 구매중 이거나 구매완료된 포토카드의 리스트를 보여준다.
    - 최근 구매한 순서로 정렬
    """

    serializer_class = BuyListSerializer
    queryset = SaleHistory.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["photocard/buy"])
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(buyer_id=request.user.id)
        qs = qs.order_by("state", "-sold_date")
        qs = self.filter_queryset(qs)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
