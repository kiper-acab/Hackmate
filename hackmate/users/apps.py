__all__ = []

import django.apps


class UsersConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"

    def ready(self):
        __import__("users.signals")
