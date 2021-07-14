from django.contrib.auth import get_user_model

from Book.models import Book, UserBookRelation


User = get_user_model()


class Data:
    def create_user(self):
        """Создание пользователя

        Returns:
            user: сущность класса User
        """
        self.user = User.objects.create(username="Test_User", password="qwe123QWE123")

        return self.user

    def create_users(self):
        """Создание пользователей

        Returns:
            user: сущность класса User
        """
        self.user_1 = User.objects.create(
            username="Test_User_1", password="qwe123QWE123"
        )
        self.user_2 = User.objects.create(
            username="Test_User_2", password="qwe123QWE123"
        )
        self.user_3 = User.objects.create(
            username="Test_User_3", password="qwe123QWE123"
        )
        self.user_4 = User.objects.create(
            username="Test_User_4", password="qwe123QWE123"
        )
        self.user_5 = User.objects.create(
            username="Test_User_5", password="qwe123QWE123"
        )

        return self.user_1

    def delete_users(self):
        """Удаление всех пользователей"""
        User.objects.all().delete()

    def create_book(self):
        """Создание книги

        Returns:
            book: сущность класса Book
        """
        self.book = Book.objects.create(
            name="Test book",
            description="Description book",
            price=100,
            author=f"{self.user.username} T.T.",
            owner=self.user,
        )

        return self.book

    def create_books(self):
        """Создание книг

        Returns:
            book: сущность класса Book
        """
        self.book_1 = Book.objects.create(
            name="Test book 1",
            description="Description book 1",
            price=250,
            author=f"{self.user_1.username} T.T.",
            owner=self.user_1,
        )
        self.book_2 = Book.objects.create(
            name="Test book 2",
            description="Description book 2",
            price=500.99,
            author=f"{self.user_1.username} T.T.",
            owner=self.user_1,
        )
        self.book_3 = Book.objects.create(
            name="Test book 3",
            description="Description book 3",
            price=750.99,
            author=f"{self.user_1.username} T.T.",
            owner=self.user_1,
        )
        self.book_4 = Book.objects.create(
            name="Test book 4",
            description="Description book 4",
            price=1000,
            author=f"{self.user_1.username} T.T.",
            owner=self.user_1,
        )
        self.book_5 = Book.objects.create(
            name="Test book 5",
            description="Description book 5",
            price=1000,
            author=f"{self.user_2.username} T.T.",
            owner=self.user_2,
        )
        self.book_6 = Book.objects.create(
            name="Test book 6",
            description="Description book 6",
            price=1000,
            author=f"{self.user_3.username} T.T.",
            owner=self.user_3,
        )
        self.book_7 = Book.objects.create(
            name="Test book 7",
            description="Description book 7",
            price=1000,
            author=f"{self.user_4.username} T.T.",
            owner=self.user_4,
        )
        self.book_8 = Book.objects.create(
            name="Test book 8",
            description="Description book 8",
            price=1000,
            author=f"{self.user_5.username} T.T.",
            owner=self.user_5,
        )

        return self.book_1

    def delete_books(self):
        """Удаление всех книг"""
        Book.objects.all().delete()

    def create_userbookrelation(self):
        """Создание связи пользователь-книга

        Returns:
            userbookrelation: сущность класса UserBookRelation
        """
        self.userbookrelation = UserBookRelation.objects.create(
            user=self.user, book=self.book, like=True, favorites=True, rating=5
        )

        return self.userbookrelation

    def create_userbookrelations(self):
        """Создание связей  пользователь-книга

        Returns:
            userbookrelation: сущность класса UserBookRelation
        """
        self.userbookrelation_1 = UserBookRelation.objects.create(
            user=self.user_2, book=self.book_1, like=True, favorites=True, rating=5
        )

        self.userbookrelation_2 = UserBookRelation.objects.create(
            user=self.user_3, book=self.book_1, like=False, favorites=True, rating=5
        )

        self.userbookrelation_3 = UserBookRelation.objects.create(
            user=self.user_4, book=self.book_1, like=False, favorites=False, rating=5
        )

        self.userbookrelation_4 = UserBookRelation.objects.create(
            user=self.user_5, book=self.book_1, like=False, favorites=False, rating=None
        )

        return self.userbookrelation_1


    def delete_userbookrelations(self):
        """Удаление всех связей"""
        UserBookRelation.objects.all().delete()

    def create_all(self):
        """Создание пользователей, книг, связей пользователь-книга

        Returns:
            list: сущности классов User, Book, UserBookRelation
        """
        self.create_users()
        self.create_books()
        self.create_userbookrelations()

        return [self.create_users, self.create_books, self.create_userbookrelations()]

    def delete_all(self):
        """Удаление всех связей пользователь-книга, книга, пользователь"""
        self.delete_userbookrelations()
        self.delete_books()
        self.delete_users()
