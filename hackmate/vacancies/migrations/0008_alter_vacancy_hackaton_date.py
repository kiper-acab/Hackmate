__all__ = ()

import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0007_alter_vacancy_unique_together"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="hackaton_date",
            field=django.db.models.DateField(
                help_text="Введите дата проведения хакатона",
                verbose_name="дата проведения хакатона",
            ),
        ),
    ]
