__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0007_alter_vacancy_hackaton_date"),
    ]

    operations = [
        django.db.migrations.AlterUniqueTogether(
            name="vacancy",
            unique_together={("title", "hackaton_title")},
        ),
    ]
