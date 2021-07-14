from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Book, UserBookRelation
from .serializers import BookSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["price"]
    search_fields = ["name", "author"]
    ordering_fields = ["price", "author"]


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "book"

    def get_object(self):
        obj, status = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs["book"]
        )

        return obj