from django.test import TestCase
from django.contrib.auth import get_user_model

from Book.models import Book, UserBookRelation
from Book.serializers import BookSerializer, OwnerSerializer, UserBookRelationSerializer
from .data_test import Data


User = get_user_model()


class TestSerializers(TestCase):
    def setUp(self):
        self.init_data = Data()
        self.init_data.create_all()

    def test_owner_serialize(self):
        """Проверка полей сериализатора OwnerSerializer"""
        users = User.objects.all()
        data = OwnerSerializer([user for user in users], many=True).data
        needed_data = []

        for user in users:
            needed_data.append(
                {
                    "id": user.id,
                    "username": user.username,
                }
            )

        self.assertEqual(needed_data, data)

    def test_book_serialize(self):
        """Проверка полей сериализатора BookSerializer"""
        books = Book.objects.all()
        data = BookSerializer([book for book in books], many=True).data
        needed_data = []

        for book in books:
            needed_data.append(
                {
                    "id": book.id,
                    "name": book.name,
                    "description": book.description,
                    "price": f"{book.price}",
                    "author": book.author,
                    "owner": {
                        "id": book.owner.id,
                        "username": book.owner.username,
                    },
                    "reader": list(user.id for user in book.reader.all()),
                }
            )

        self.assertEqual(needed_data, data)

    def test_userbookrelation_serializer(self):
        """Проверка полей сериализатора UserBookRelation"""
        relations = UserBookRelation.objects.all()
        data = UserBookRelationSerializer(
            [relation for relation in relations], many=True
        ).data
        needed_data = []

        for relation in relations:
            needed_data.append(
                {
                    "book": relation.book.id,
                    "like": relation.like,
                    "favorites": relation.favorites,
                    "rating": relation.rating,
                }
            )

        self.assertEqual(needed_data, data)

    def tearDown(self):
        self.init_data.delete_all()
