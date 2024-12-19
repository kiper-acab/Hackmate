__all__ = ()

import django.apps
import django.utils.translation


class ApiConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    verbose_name = django.utils.translation.gettext_lazy("Апи")
