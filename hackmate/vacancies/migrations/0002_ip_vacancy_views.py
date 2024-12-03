__all__ = ()

import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0001_initial"),
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
        ),
        django.db.migrations.AddField(
            model_name="vacancy",
            name="views",
            field=django.db.models.ManyToManyField(
                blank=True,
                related_name="post_views",
                to="vacancies.ip",
            ),
        ),
    ]
