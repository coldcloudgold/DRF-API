from django.contrib import admin
from .models import Book, UserBookRelation


class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "author")
    search_fields = ("name", "author")
    empty_value_display = "-пусто-"


class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "like", "favorites", "rating")
    search_fields = ("user", "book")
    list_filter = ("like", "favorites")
    empty_value_display = "-пусто-"


admin.site.register(Book, BookAdmin)
admin.site.register(UserBookRelation, UserBookRelationAdmin)
