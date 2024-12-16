__all__ = ()

import django.apps


class NotifyConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notify"
    verbose_name = "Уведомления"

    def ready(self):
        __import__("notify.signals")
