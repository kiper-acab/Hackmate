__all__ = ()

import django.core.validators
import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0006_vacancy_deadline_vacancy_required_experience"),
    ]

    operations = [
        django.db.migrations.AddField(
            model_name="vacancy",
            name="role",
            field=django.db.models.CharField(
                choices=[
                    ("Разработчик", "Разработчик"),
                    ("Дизайнер", "Дизайнер"),
                    ("Проектный менеджер", "Проектный менеджер"),
                    ("Тестировщик", "Тестировщик"),
                    ("Другая роль", "Другая роль"),
                ],
                default="Другая роль",
                max_length=50,
                verbose_name="Роль",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="required_experience",
            field=django.db.models.IntegerField(
                blank=True,
                help_text="Укажите количество лет опыта, "
                "необходимого для кандидата",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="требуемый опыт (в годах)",
            ),
        ),
    ]
