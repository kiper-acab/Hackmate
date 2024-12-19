__all__ = ()

import django.conf
import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        django.db.migrations.swappable_dependency(
            django.conf.settings.AUTH_USER_MODEL,
        ),
        ("vacancies", "0002_alter_commentvacancy_comment_and_more"),
    ]

    operations = [
        django.db.migrations.AlterUniqueTogether(
            name="response",
            unique_together=set(),
        ),
        django.db.migrations.AddField(
            model_name="response",
            name="status",
            field=django.db.models.CharField(
                choices=[
                    ("accepted", "accepted"),
                    ("rejected", "rejected"),
                    ("not_answered", "not_answered"),
                ],
                default="not_answered",
                max_length=255,
            ),
        ),
        django.db.migrations.AddField(
            model_name="vacancy",
            name="team_composition",
            field=django.db.models.ManyToManyField(
                related_name="team_composition",
                to=django.conf.settings.AUTH_USER_MODEL,
                verbose_name="состав команды",
            ),
        ),
    ]
