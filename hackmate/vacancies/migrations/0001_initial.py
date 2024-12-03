__all__ = ()

import django.conf
import django.db
import django.db.models.deletion


class Migration(django.db.migrations.Migration):

    initial = True

    dependencies = [
        django.db.migrations.swappable_dependency(
            django.conf.settings.AUTH_USER_MODEL,
        ),
    ]

    operations = [
        django.db.migrations.CreateModel(
            name="Vacancy",
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
                    "title",
                    django.db.models.CharField(
                        max_length=255,
                        verbose_name="название вакансии",
                    ),
                ),
                (
                    "description",
                    django.db.models.TextField(
                        verbose_name="описание вакансии",
                    ),
                ),
                (
                    "created_at",
                    django.db.models.DateTimeField(auto_now_add=True),
                ),
                ("updated_at", django.db.models.DateTimeField(auto_now=True)),
                (
                    "status",
                    django.db.models.CharField(
                        choices=[
                            ("active", "active"),
                            ("finished", "finished"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "creater",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="создатель вакансии",
                    ),
                ),
            ],
            options={
                "verbose_name": "вакансия",
                "verbose_name_plural": "вакансии",
            },
        ),
    ]
