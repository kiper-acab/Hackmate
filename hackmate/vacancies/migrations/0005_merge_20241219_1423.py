__all__ = ()

import django.db


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("vacancies", "0003_alter_vacancy_required_experience"),
        ("vacancies", "0004_vacancy_need_count_users_alter_vacancy_status"),
    ]

    operations = []
