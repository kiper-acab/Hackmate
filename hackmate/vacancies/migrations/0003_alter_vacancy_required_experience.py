__all__ = ()

import django.core.validators
import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0002_alter_vacancy_description"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="required_experience",
            field=django.db.models.IntegerField(
                blank=True,
                help_text="Укажите количество лет опыта, "
                "необходимого для кандидата",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(10),
                ],
                verbose_name="требуемый опыт (в годах)",
            ),
        ),
    ]
