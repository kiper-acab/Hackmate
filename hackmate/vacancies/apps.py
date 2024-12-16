__all__ = ()

import django.apps
import django.utils.translation


class VacanciesConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vacancies"
    verbose_name = django.utils.translation.gettext_lazy("Вакансии")
