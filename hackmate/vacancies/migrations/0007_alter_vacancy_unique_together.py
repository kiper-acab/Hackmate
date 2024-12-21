__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        (
            "vacancies",
            "0006_alter_response_options_remove_vacancy_deadline_and_more",
        ),
    ]

    operations = [
        django.db.migrations.AlterUniqueTogether(
            name="vacancy",
            unique_together={("title", "hackaton_title")},
        ),
    ]
