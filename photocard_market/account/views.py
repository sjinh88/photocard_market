from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserWallet
from .serializers import (LoginSerializer, RegisterSerializer,
                          UserWalletSerializer)


class RegisterAPIView(generics.CreateAPIView):
    """
    회원가입
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginAPIView(generics.GenericAPIView):
    """
    로그인
    - jwt 토큰 생성 (access/refresh)
    - 생성된 토큰은 cookie로 전달
    """

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            raise ValidationError(serializer.errors)

        email = serializer.data["email"]
        password = serializer.initial_data["password"]

        # user, password 확인
        user = authenticate(username=email, password=password)
        if user is None:
            raise ValidationError({"password": "패스워드가 맞지 않습니다."})

        # user 상태 확인
        if not user.is_active:
            raise ValidationError({"user": "탈퇴한 회원입니다."})

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # jwt 토큰 생성
        # 생성된 토큰은 body가 아닌 쿠키로 전달
        token = TokenObtainPairSerializer.get_token(user)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(key="access", value=str(token.access_token), httponly=True)
        response.set_cookie(key="refresh", value=str(token), httponly=True)

        return response


class UserWalletAPIVIew(generics.RetrieveAPIView):

    queryset = UserWallet.objects.all()
    serializer_class = UserWalletSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "user_id"

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().get(user_id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
