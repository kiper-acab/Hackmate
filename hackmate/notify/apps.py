__all__ = ()

import django.apps
import django.utils.translation


class NotifyConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notify"
    verbose_name = django.utils.translation.gettext_lazy("Уведомления")

    def ready(self):
        __import__("notify.signals")
