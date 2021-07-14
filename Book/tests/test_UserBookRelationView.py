import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail

from Book.models import UserBookRelation
from Book.serializers import UserBookRelationSerializer
from .data_test import Data


class TestUserBookRelationUpdateAUTH(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.user = self.init_data.create_user()
        self.book = self.init_data.create_book()
        self.user_book_relation = self.init_data.create_userbookrelation()
        self.url_detail = reverse(
            "userbookrelation-detail", args=(self.user_book_relation.book.id,)
        )
        self.client.force_login(self.user)

    def test_put(self):
        """Проверка измениния связи пользователя с книгой (PUT)"""
        data = {
            "id": self.user_book_relation.id,
            "user": self.user.id,
            "book": self.book.id,
            "like": False,
            "favorites": False,
            "rating": None,
        }

        json_data = json.dumps(data)

        response = self.client.put(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        needed_data = UserBookRelationSerializer(UserBookRelation.objects.last()).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data)

    def test_patch(self):
        """Проверка измениния связи пользователя с книгой (PATCH)"""
        data = {
            "like": False,
            "favorites": False,
            "rating": None,
        }

        json_data = json.dumps(data)

        response = self.client.patch(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        self.user_book_relation.refresh_from_db()
        needed_data = UserBookRelationSerializer(self.user_book_relation).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data)


class TestUserBookRelationUpdateNoAUTH(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.user = self.init_data.create_user()
        self.book = self.init_data.create_book()
        self.user_book_relation = self.init_data.create_userbookrelation()
        self.url_detail = reverse(
            "userbookrelation-detail", args=(self.user_book_relation.book.id,)
        )
        self.response_data = {
            "detail": ErrorDetail(
                string="Учетные данные не были предоставлены.", code="not_authenticated"
            )
        }

    def test_put(self):
        """Проверка измениния связи пользователя с книгой (PUT)"""
        data = {
            "id": self.user_book_relation.id,
            "user": self.user.id,
            "book": self.book.id,
            "like": False,
            "favorites": False,
            "rating": None,
        }

        json_data = json.dumps(data)

        response = self.client.put(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(self.response_data, response.data)

    def test_patch(self):
        """Проверка измениния связи пользователя с книгой (PATCH)"""
        data = {
            "like": False,
            "favorites": False,
            "rating": None,
        }

        json_data = json.dumps(data)

        response = self.client.patch(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(self.response_data, response.data)
