__all__ = ()

import django.conf
import django.db
import django.db.models.deletion


class Migration(django.db.migrations.Migration):

    dependencies = [
        django.db.migrations.swappable_dependency(
            django.conf.settings.AUTH_USER_MODEL,
        ),
        ("vacancies", "0003_response"),
    ]

    operations = [
        django.db.migrations.AddField(
            model_name="vacancy",
            name="hackaton_title",
            field=django.db.models.CharField(
                blank=True,
                help_text="Название хакатона, к которому относится вакансия",
                max_length=255,
                null=True,
                verbose_name="название хакатона",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="created_at",
            field=django.db.models.DateTimeField(
                auto_now_add=True,
                verbose_name="создано",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="status",
            field=django.db.models.CharField(
                choices=[("active", "active"), ("finished", "finished")],
                max_length=255,
                verbose_name="cтатус",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="updated_at",
            field=django.db.models.DateTimeField(
                auto_now=True,
                verbose_name="обновлено",
            ),
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
            },
        ),
    ]
