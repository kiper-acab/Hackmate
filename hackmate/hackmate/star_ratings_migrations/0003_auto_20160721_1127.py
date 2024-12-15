__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("star_ratings", "0002_auto_20160608_1119"),
    ]

    operations = [
        django.db.migrations.AlterUniqueTogether(
            name="userrating",
            unique_together=set([("user", "rating")]),
        ),
    ]
