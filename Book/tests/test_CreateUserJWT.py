from rest_framework import status
from rest_framework.test import APITestCase


class TestUser(APITestCase):
    data = {"username": "Ivan", "password": "Ivanov12345"}

    def test_create_user(self):
        """Проверка создания пользователя, токена"""
        response = self.client.post(
            "/auth/users/",
            data=self.data,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(bool(response.data["username"]))

        response = self.client.post(
            "/auth/jwt/create/",
            data=self.data,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(
            bool(response.data["refresh"]) and bool(response.data["access"])
        )
