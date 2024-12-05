__all__ = ()

import django.conf
import django.db
import django.db.models.deletion


class Migration(django.db.migrations.Migration):

    dependencies = [
        django.db.migrations.swappable_dependency(
            django.conf.settings.AUTH_USER_MODEL,
        ),
        ("vacancies", "0002_ip_vacancy_views"),
    ]

    operations = [
        django.db.migrations.CreateModel(
            name="Response",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    django.db.models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата отклика",
                    ),
                ),
                (
                    "user",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "vacancy",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="vacancies.vacancy",
                        verbose_name="Вакансия",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отклик",
                "verbose_name_plural": "Отклики",
                "unique_together": {("user", "vacancy")},
            },
        ),
    ]
