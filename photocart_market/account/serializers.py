from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    회원가입 serializer
    """

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],  # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호 검증
    )
    password2 = serializers.CharField(  # 비밀번호 확인용
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
        user = User.objects.create_user(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    로그인 serializer
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def validate(self, value: dict) -> dict:
        """
        email 기반 user 검증
        """
        # email 존재 여부 확인
        user = User.objects.filter(email=value["email"])
        if not user.exists():
            raise serializers.ValidationError({"user": "회원가입이 필요합니다."})

        # email 휴면 계정 여부 확인
        user = user.first()
        if not user.is_active:
            raise serializers.ValidationError({"user": "휴먼 계정입니다."})

        return value
