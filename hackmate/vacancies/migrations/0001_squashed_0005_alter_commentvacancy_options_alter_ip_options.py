__all__ = ()

import django.conf
import django.db
import django.db.models.deletion


class Migration(django.db.migrations.Migration):

    replaces = [
        ("vacancies", "0001_initial"),
        ("vacancies", "0002_ip_vacancy_views"),
        ("vacancies", "0003_response"),
        (
            "vacancies",
            "0004_vacancy_hackaton_title_alter_vacancy_created_at_and_more",
        ),
        ("vacancies", "0005_alter_commentvacancy_options_alter_ip_options"),
    ]

    initial = True

    dependencies = [
        django.db.migrations.swappable_dependency(
            django.conf.settings.AUTH_USER_MODEL,
        ),
    ]

    operations = [
        django.db.migrations.CreateModel(
            name="Ip",
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
                ("ip", django.db.models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "IP адрес",
                "verbose_name_plural": "IP адреса",
            },
        ),
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
                    django.db.models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="создано",
                    ),
                ),
                (
                    "updated_at",
                    django.db.models.DateTimeField(
                        auto_now=True,
                        verbose_name="обновлено",
                    ),
                ),
                (
                    "status",
                    django.db.models.CharField(
                        choices=[
                            ("active", "active"),
                            ("finished", "finished"),
                        ],
                        max_length=255,
                        verbose_name="cтатус",
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
                (
                    "views",
                    django.db.models.ManyToManyField(
                        blank=True,
                        related_name="post_views",
                        to="vacancies.ip",
                    ),
                ),
                (
                    "hackaton_title",
                    django.db.models.CharField(
                        blank=True,
                        help_text=(
                            "Название хакатона, к которому относится вакансия"
                        ),
                        max_length=255,
                        null=True,
                        verbose_name="название хакатона",
                    ),
                ),
            ],
            options={
                "verbose_name": "вакансия",
                "verbose_name_plural": "вакансии",
            },
        ),
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
        django.db.migrations.CreateModel(
            name="CommentVacancy",
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
                    "comment",
                    django.db.models.TextField(verbose_name="комментарий"),
                ),
                (
                    "created_at",
                    django.db.models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="cоздано",
                    ),
                ),
                (
                    "user",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
                (
                    "vacancy",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="vacancies.vacancy",
                        verbose_name="вакансия",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "комментарий к вакансии",
                "verbose_name_plural": "комментарии к вакансиям",
            },
        ),
    ]
