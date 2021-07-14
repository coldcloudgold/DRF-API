from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.CharField(max_length=500, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    author = models.CharField(max_length=150, verbose_name="Автор")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="own_books",
        verbose_name="Владелец",
    )
    reader = models.ManyToManyField(
        User,
        through="UserBookRelation",
        related_name="read_books",
        verbose_name="Читатель",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class UserBookRelation(models.Model):
    RAITING_CHOISE = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_books",
        verbose_name="Пользователь",
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="user_books", verbose_name="Книга"
    )
    like = models.BooleanField(default=False, verbose_name="Нравится")
    favorites = models.BooleanField(default=False, verbose_name="Избранное")
    rating = models.PositiveSmallIntegerField(
        choices=RAITING_CHOISE, blank=True, null=True, verbose_name="Оценка"
    )

    def __str__(self):
        return f"U: {self.user}; B: {self.book}"

    class Meta:
        verbose_name = "Пользователь и книга"
        verbose_name_plural = "Пользователи и книги"
