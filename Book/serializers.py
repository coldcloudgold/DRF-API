from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from django.contrib.auth import get_user_model
from .models import Book, UserBookRelation


User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class BookSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"


class UserBookRelationSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "favorites", "rating")