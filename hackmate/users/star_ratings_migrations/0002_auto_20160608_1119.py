__all__ = ()

import django.conf
import django.db
import django.db.models.deletion


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("star_ratings", "0001_initial"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="userrating",
            name="user",
            field=django.db.models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=django.conf.settings.AUTH_USER_MODEL,
            ),
        ),
        django.db.migrations.AlterUniqueTogether(
            name="userrating",
            unique_together=set([("user", "rating", "ip")]),
        ),
    ]
