__all__ = ()

import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        (
            "vacancies",
            "0006_alter_response_options_remove_vacancy_deadline_and_more",
        ),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="hackaton_date",
            field=django.db.models.DateField(
                help_text="Введите крайний срок подачи заявок",
                verbose_name="Крайний срок подачи заявок",
            ),
        ),
    ]
