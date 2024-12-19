__all__ = ()


import decimal

import django.conf
import django.db
import django.db.models
import django.utils.timezone
import model_utils.fields
import swapper


dependancies = [
    django.db.migrations.swappable_dependency(
        django.conf.settings.AUTH_USER_MODEL,
    ),
    ("contenttypes", "0001_initial"),
]

swappable_dep = swapper.dependency("star_ratings", "Rating")
if swappable_dep == (
    django.db.migrations.swappable_dependency("star_ratings.Rating")
):
    dependancies.append(swappable_dep)


class Migration(django.db.migrations.Migration):
    dependencies = dependancies

    operations = [
        django.db.migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    django.db.models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("count", django.db.models.PositiveIntegerField(default=0)),
                ("total", django.db.models.PositiveIntegerField(default=0)),
                (
                    "average",
                    django.db.models.DecimalField(
                        decimal_places=3,
                        max_digits=6,
                        default=decimal.Decimal("0"),
                    ),
                ),
                (
                    "object_id",
                    django.db.models.PositiveIntegerField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    "content_type",
                    django.db.models.ForeignKey(
                        blank=True,
                        null=True,
                        to="contenttypes.ContentType",
                        on_delete=django.db.models.CASCADE,
                    ),
                ),
            ],
            options={
                "swappable": swapper.swappable_setting(
                    "star_ratings",
                    "Rating",
                ),
            },
            bases=(django.db.models.Model,),
        ),
        django.db.migrations.CreateModel(
            name="UserRating",
            fields=[
                (
                    "id",
                    django.db.models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        verbose_name="created",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        verbose_name="modified",
                        editable=False,
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "ip",
                    django.db.models.GenericIPAddressField(
                        blank=True,
                        null=True,
                    ),
                ),
                ("score", django.db.models.PositiveSmallIntegerField()),
                (
                    "rating",
                    django.db.models.ForeignKey(
                        related_name="user_ratings",
                        to=swapper.get_model_name("star_ratings", "Rating"),
                        on_delete=django.db.models.CASCADE,
                    ),
                ),
                (
                    "user",
                    django.db.models.ForeignKey(
                        to=django.conf.settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(django.db.models.Model,),
        ),
        django.db.migrations.AlterUniqueTogether(
            name="userrating",
            unique_together=set([("user", "rating")]),
        ),
        django.db.migrations.AlterUniqueTogether(
            name="rating",
            unique_together=set([("content_type", "object_id")]),
        ),
    ]
