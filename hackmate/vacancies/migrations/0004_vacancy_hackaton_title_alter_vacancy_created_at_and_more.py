__all__ = ()

import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
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
    ]