from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Book"
    verbose_name = "Книга"

    def ready(self):
        try:
            import os
            from django.db.models import Q
            from django.contrib.auth import get_user_model

            User = get_user_model()

            if not User.objects.filter(
                username=os.environ.get("ADMIN_NAME", "admin")
            ).exists():
                user_admin = User.objects.create_user(
                    username=os.environ.get("ADMIN_NAME", "admin"),
                    password=os.environ.get("ADMIN_PASSWORD", "admin"),
                )
                user_admin.is_superuser = True
                user_admin.is_staff = True
                user_admin.save()
        except Exception as exc:
            pass
