__all__ = ()

import django.core.validators
import django.db
import django.db.models
import tinymce.models


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0005_merge_20241219_1423"),
    ]

    operations = [
        django.db.migrations.AlterModelOptions(
            name="response",
            options={
                "ordering": ["-created_at", "id"],
                "verbose_name": "отклик",
                "verbose_name_plural": "отклики",
            },
        ),
        django.db.migrations.RenameField(
            model_name="vacancy",
            old_name="deadline",
            new_name="hackaton_date",
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="description",
            field=tinymce.models.HTMLField(
                help_text="Описание вакансии должно быть "
                "от 5 до 10000 символов",
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
            field=django.db.models.CharField(
                choices=[
                    ("no_expirience", "Нет опыта"),
                    ("up_to_6_months", "До 6 месяцев"),
                    ("6_to_12_months", "От 6 до 12 месяцев"),
                    ("more_than_12_months", "Более 1 года"),
                ],
                default="no_expirience",
                help_text="Укажите количество опыта необходимого "
                "для кандидата",
                max_length=300,
                verbose_name="требуемый опыт",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="vacancy",
            name="status",
            field=django.db.models.CharField(
                choices=[
                    ("active", "active"),
                    ("equipped", "equipped"),
                    ("deleted", "deleted"),
                ],
                max_length=255,
                verbose_name="cтатус",
            ),
        ),
    ]
