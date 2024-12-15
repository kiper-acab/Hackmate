__all__ = ()

import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("star_ratings", "0003_auto_20160721_1127"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="rating",
            name="id",
            field=django.db.models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="userrating",
            name="id",
            field=django.db.models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
