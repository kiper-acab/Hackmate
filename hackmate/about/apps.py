__all__ = ()

import django.apps
import django.utils.translation


class AboutConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
    verbose_name = django.utils.translation.gettext_lazy("О проекте")
