__all__ = []

import django.apps
import django.utils.translation


class UsersConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = django.utils.translation.gettext_lazy("Пользователи")

    def ready(self):
        __import__("users.signals")
