__all__ = ()

import django.core.validators
import django.db
import django.db.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0001_initial"),
    ]

    operations = [
        django.db.migrations.AlterField(
            model_name="commentvacancy",
            name="comment",
            field=django.db.models.TextField(
                validators=[
                    django.core.validators.MinLengthValidator(
                        5,
                        "Слишком короткий комментарий!",
                    ),
                    django.core.validators.MaxLengthValidator(
                        3000,
                        "Комментарий не может привышать 3000 символов!",
                    ),
                ],
                verbose_name="комментарий",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="description",
            field=django.db.models.TextField(
                help_text=(
                    "Описание вакансии должно " "быть от 5 до 10000 символов"
                ),
                validators=[
                    django.core.validators.MinLengthValidator(
                        5,
                        "Описание не может быть таким коротким",
                    ),
                    django.core.validators.MaxLengthValidator(
                        10000,
                        "Описание не может быть таким длинным",
                    ),
                ],
                verbose_name="описание вакансии",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="required_experience",
            field=django.db.models.IntegerField(
                blank=True,
                help_text=(
                    "Укажите количество лет опыта "
                    "необходимого для кандидата"
                ),
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(
                        0,
                        "Введите корректное значение",
                    ),
                    django.core.validators.MaxValueValidator(
                        100,
                        "Введите корректное значение",
                    ),
                ],
                verbose_name="требуемый опыт (в годах)",
            ),
        ),
    ]
