__all__ = ()

import django.apps


class VacanciesConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vacancies"
    verbose_name = "Вакансии"

    def ready(self):
        __import__("vacancies.signals")
