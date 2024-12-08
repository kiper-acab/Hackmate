__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        (
            "vacancies",
            "0004_vacancy_hackaton_title_alter_vacancy_created_at_and_more",
        ),
    ]

    operations = [
        django.db.migrations.AlterModelOptions(
            name="commentvacancy",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "комментарий к вакансии",
                "verbose_name_plural": "комментарии к вакансиям",
            },
        ),
        django.db.migrations.AlterModelOptions(
            name="ip",
            options={
                "verbose_name": "IP адрес",
                "verbose_name_plural": "IP адреса",
            },
        ),
    ]
