from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AccountAPITests(APITestCase):

    def setUp(self):
        self.login_url = "/account/login/"
        user = User.objects.create(email="kaero88@naver.com")
        user.set_password("tlswlsgh1A!")
        user.save()

    def test_user_login(self):
        # 정상 로그인 체크
        login_data = {"email": "kaero88@naver.com", "password": "tlswlsgh1A!"}
        # POST 요청을 보냅니다.
        response = self.client.post(self.login_url, login_data, format="json")
        # 응답 상태 코드가 200인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid(self):
        # 비밀번호 틀림
        login_data = {"email": "kaero88@naver.com", "password": "tlswlsgh1A!"}

        # POST 요청을 보냅니다.
        response = self.client.post(self.login_url, login_data, format="json")
        # 응답 상태 코드가 400인지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
