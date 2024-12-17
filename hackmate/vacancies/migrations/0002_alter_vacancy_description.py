__all__ = ()

import django.db
import tinymce.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0001_initial"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="description",
            field=tinymce.models.HTMLField(verbose_name="описание вакансии"),
        ),
    ]
