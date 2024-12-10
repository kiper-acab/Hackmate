__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0005_alter_commentvacancy_options_alter_ip_options"),
    ]

    operations = [
        django.db.migrations.AddField(
            model_name="vacancy",
            name="deadline",
            field=django.db.models.DateField(
                blank=True,
                help_text="Крайний срок подачи заявок",
                null=True,
                verbose_name="дедлайн",
            ),
        ),
        django.db.migrations.AddField(
            model_name="vacancy",
            name="required_experience",
            field=django.db.models.IntegerField(
                blank=True,
                help_text="Укажите количество лет опыта, "
                "необходимого для кандидата",
                null=True,
                verbose_name="требуемый опыт (в годах)",
            ),
        ),
    ]
