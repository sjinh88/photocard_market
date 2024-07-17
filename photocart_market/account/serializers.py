from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],  # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField(  # 비밀번호 확인을 위한 필드
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "password", "password2"]

    def validate(self, data: dict) -> dict:
        # password과 password2의 일치 여부 확인
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "입력한 패스워드가 일치하지 않습니다."}
            )

        return data

    def create(self, validated_data: dict) -> User:
        # CREATE 요청에 대해 create 메서드를 오버라이딩하여,
        # 유저를 생성하고 토큰도 생성하게 해준다.
        user = User.objects.create_user(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def validate(self, value):
        user = User.objects.filter(email=value["email"])
        if not user.exists():
            raise serializers.ValidationError({"user": "회원가입이 필요합니다."})

        user = user.first()
        if not user.is_active:
            raise serializers.ValidationError({"user": "휴먼 계정입니다."})

        return value
