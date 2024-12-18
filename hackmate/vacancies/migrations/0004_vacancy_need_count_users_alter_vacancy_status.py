__all__ = ()

import django.core.validators
import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        (
            "vacancies",
            "0003_alter_response_unique_together_response_status_and_more",
        ),
    ]

    operations = [
        django.db.migrations.AddField(
            model_name="vacancy",
            name="need_count_users",
            field=django.db.models.PositiveSmallIntegerField(
                default=3,
                validators=[
                    django.core.validators.MinValueValidator(
                        2,
                        "Введите корректное значение",
                    ),
                    django.core.validators.MaxValueValidator(
                        100,
                        "Введите корректное значение",
                    ),
                ],
                verbose_name=(
                    "необходимое количество человек "
                    "в группе для участия в хакатоне"
                ),
            ),
            preserve_default=False,
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="status",
            field=django.db.models.CharField(
                choices=[
                    ("active", "active"),
                    ("inactive", "inactive"),
                    ("deleted", "deleted"),
                ],
                max_length=255,
                verbose_name="cтатус",
            ),
        ),
    ]
