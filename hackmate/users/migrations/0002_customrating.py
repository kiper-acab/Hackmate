__all__ = ()

import django.db.migrations


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        django.db.migrations.CreateModel(
            name="CustomRating",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("star_ratings.rating",),
        ),
    ]
