from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import exceptions, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializers import LoginSerializer, RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginAPIView(generics.GenericAPIView):
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
