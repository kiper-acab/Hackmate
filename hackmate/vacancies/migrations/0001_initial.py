__all__ = ()

import django.conf
import django.core.validators
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
                            ("inactive", "inactive"),
                        ],
                        max_length=255,
                        verbose_name="cтатус",
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
                (
                    "deadline",
                    django.db.models.DateField(
                        blank=True,
                        help_text="Крайний срок подачи заявок",
                        null=True,
                        verbose_name="дедлайн",
                    ),
                ),
                (
                    "required_experience",
                    django.db.models.IntegerField(
                        blank=True,
                        help_text=(
                            "Укажите количество лет опыта, "
                            "необходимого для кандидата"
                        ),
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="требуемый опыт (в годах)",
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
            ],
            options={
                "verbose_name": "вакансия",
                "verbose_name_plural": "вакансии",
                "ordering": ["-created_at"],
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
                "verbose_name": "комментарий к вакансии",
                "verbose_name_plural": "комментарии к вакансиям",
                "ordering": ["-created_at"],
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
                        verbose_name="дата отклика",
                    ),
                ),
                (
                    "user",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
                (
                    "vacancy",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="vacancies.vacancy",
                        verbose_name="вакансия",
                    ),
                ),
            ],
            options={
                "verbose_name": "отклик",
                "verbose_name_plural": "отклики",
                "unique_together": {("user", "vacancy")},
            },
        ),
    ]
