__all__ = ()

import django.apps
import django.utils.translation


class HomepageConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = django.utils.translation.gettext_lazy("Главная страница")
