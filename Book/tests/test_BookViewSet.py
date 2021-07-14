import json

from django.urls import reverse
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail

from Book.models import Book
from Book.serializers import BookSerializer
from .data_test import Data


class TestBookViewSetField(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.init_data.create_all()
        self.url = reverse("book-list")

    def test_queryfields(self):
        """Проверка полученных данных с запрашиваемыми полями (id, name, price)"""
        books = Book.objects.all()
        needed_data = []

        for book in books:
            needed_data.append(
                {
                    "id": book.id,
                    "name": book.name,
                    "price": f"{book.price}",
                }
            )

        response = self.client.get(self.url, data={"fields": "id,name,price"})

        self.assertEqual(needed_data, response.data["results"])

    def test_filter(self):
        """Проверка полученных данных с фильтром по полю (price)"""
        filter_data = 500.99

        needed_data = BookSerializer(
            [book for book in Book.objects.filter(price=filter_data)], many=True
        ).data

        response = self.client.get(self.url, data={"price": str(filter_data)})

        self.assertEqual(needed_data, response.data["results"])

    def test_search(self):
        """Проверка полученных данных с поиском по полям (name, author)"""
        search_data = "1"

        needed_data = BookSerializer(
            [
                book
                for book in Book.objects.filter(
                    Q(name__icontains=search_data) | Q(author__icontains=search_data)
                )
            ],
            many=True,
        ).data

        response = self.client.get(self.url, data={"search": search_data})

        self.assertEqual(needed_data, response.data["results"])

    def test_order(self):
        """Проверка полученных данных с сортировкой по полю (price, author)"""
        order_data = "price"

        needed_data = BookSerializer(
            [book for book in Book.objects.all().order_by(order_data)], many=True
        ).data

        response = self.client.get(self.url, data={"ordering": order_data})
        self.assertEqual(needed_data, response.data["results"])

    def tearDown(self):
        self.init_data.delete_all()


class TestBookViewSetCRUDAuth(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.user = self.init_data.create_user()
        self.book = self.init_data.create_book()
        self.url = reverse("book-list")
        self.url_detail = reverse("book-detail", args=(self.book.id,))
        self.client.force_login(self.user)

    def test_get(self):
        """Проверка полученных книг (GET)"""
        needed_data = BookSerializer(
            [book for book in Book.objects.all()], many=True
        ).data

        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data["results"])

    def test_post(self):
        """Проверка создания книги (POST)"""
        data = {
            "author": f"{self.user.username} T.T.",
            "owner": None,
            "name": "Test book create POST",
            "description": "Test book create POST",
            "price": self.book.price,
        }

        json_data = json.dumps(data)

        response = self.client.post(
            self.url, data=json_data, content_type="application/json"
        )

        needed_data = BookSerializer(Book.objects.last()).data

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(needed_data, response.data)

    def test_put(self):
        """Проверка измениния книги (PUT)"""
        data = {
            "id": self.book.id,
            "author": f"{self.user.username} T.T.",
            "owner": {
                "username": self.user.username,
                "email": self.user.email,
            },
            "name": "Test book edit PUT",
            "description": "Test book edit PUT",
            "price": self.book.price,
        }

        json_data = json.dumps(data)

        response = self.client.put(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        needed_data = BookSerializer(Book.objects.last()).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data)

    def test_patch(self):
        """Проверка измениния книги (PATCH)"""
        data = {
            "name": "Test book edit PATCH",
            "description": "Test book edit PATCH",
        }

        json_data = json.dumps(data)

        response = self.client.patch(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        self.book.refresh_from_db()
        needed_data = BookSerializer(self.book).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(needed_data, response.data)

    def test_delete(self):
        """Проверка удаления книги (DELETE)"""
        response = self.client.delete(self.url_detail)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(None, response.data)

    def tearDown(self):
        self.init_data.delete_all()


class TestBookViewSetCRUDNoAuth(APITestCase):
    def setUp(self):
        self.init_data = Data()
        self.user = self.init_data.create_user()
        self.book = self.init_data.create_book()
        self.url = reverse("book-list")
        self.url_detail = reverse("book-detail", args=(self.book.id,))
        self.response_data = {
            "detail": ErrorDetail(
                string="Учетные данные не были предоставлены.", code="not_authenticated"
            )
        }

    def test_post(self):
        """Проверка создания книги (POST)"""
        data = {
            "author": f"{self.user.username} T.T.",
            "owner": {
                "username": self.user.username,
                "email": self.user.email,
            },
            "name": "Test book create POST",
            "description": "Test book create POST",
            "price": self.book.price,
        }

        json_data = json.dumps(data)

        response = self.client.post(
            self.url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(self.response_data, response.data)

    def test_put(self):
        """Проверка измениния книги (PUT)"""
        data = {
            "id": self.book.id,
            "author": f"{self.user.username} T.T.",
            "owner": {
                "username": self.user.username,
                "email": self.user.email,
            },
            "name": "Test book edit PUT",
            "description": "Test book edit PUT",
            "price": self.book.price,
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
        """Проверка измениния книги (PATCH)"""
        data = {
            "name": "Test book edit PATCH",
            "description": "Test book edit PATCH",
        }

        json_data = json.dumps(data)

        response = self.client.patch(
            self.url_detail,
            data=json_data,
            content_type="application/json",
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(self.response_data, response.data)

    def test_delete(self):
        """Проверка удаления книги (DELETE)"""
        response = self.client.delete(self.url_detail)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(self.response_data, response.data)

    def tearDown(self):
        self.init_data.delete_all()
