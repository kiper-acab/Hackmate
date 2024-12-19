__all__ = ()

import django.db.migrations
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("users", "0002_customrating"),
    ]

    operations = [
        django.db.migrations.DeleteModel(
            name="CustomRating",
        ),
        django.db.migrations.AlterField(
            model_name="profilelink",
            name="site_type",
            field=django.db.models.CharField(
                choices=[
                    ("facebook", "Facebook"),
                    ("twitter", "Twitter"),
                    ("instagram", "Instagram"),
                    ("vk", "VK"),
                    ("gitlab", "GitLab"),
                    ("github", "GitHub"),
                ],
                max_length=20,
                verbose_name="тип сайта",
            ),
        ),
    ]
