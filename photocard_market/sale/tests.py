from account.models import User
from django.urls import reverse
from product.models import PhotoCard
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import SaleHistory

# 테스트 유저 등록
login_data = {
    "email": "kaero88@naver.com",
    "password": "tlswlsgh1A!",
}


class AccountAPITests(APITestCase):

    def setUp(self):
        self.login_url = reverse("user_login")
        self.sale_register_url = reverse("sale_register")

        user = User.objects.create(
            email=login_data["email"],
        )
        user.set_password(login_data["password"])
        user.save()

        self.token = AccessToken.for_user(user)

        PhotoCard.objects.create(name="테스트1.", description="테스트")
        PhotoCard.objects.create(name="테스트2.", description="테스트")
        PhotoCard.objects.create(name="테스트3.", description="테스트")

    def test_sale_register(self):
        """
        판매 등록 테스트
        """

        # 등록된 포토카드에 대한 판매 등록
        sale_data = {"photo_card": 1, "price": 1000}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.post(
            self.sale_register_url,
            sale_data,
            format="json",
        )
        # 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 등록되지 않은 포토카드에 대한 판매 등록
        sale_data = {"photo_card": 4, "price": 1000}
        response = self.client.post(
            self.sale_register_url,
            sale_data,
            format="json",
        )
        # 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sale_price_change(self):
        """
        판매 가격 수정
        """

        # 판매 신청
        sale_data = {"photo_card": 1, "price": 1000}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.post(
            self.sale_register_url,
            sale_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 구매 신청
        sale_change_url = reverse("sale_price_update", args=[1])
        response = self.client.put(
            path=sale_change_url,
            data={"price": 2000},
            format="json",
        )
        # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        SaleHistory.objects.filter(photo_card_id=1).update(buyer_id=1, state="B")

        response = self.client.put(
            path=sale_change_url,
            data={"price": 2000},
            format="json",
        )
        # 400 - 구매/판매중 일때는 변경 불가
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
