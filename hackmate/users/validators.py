__all__ = ()

import datetime

import django.core.exceptions
import django.utils.timezone


def validate_birthday(value):
    today = django.utils.timezone.now().date()
    oldest_allowed = today - datetime.timedelta(days=150 * 365)
    if value > today:
        raise django.core.exceptions.ValidationError(
            "Укажите корректную дату рождения.",
        )

    if value < oldest_allowed:
        raise django.core.exceptions.ValidationError(
            "Укажите корректную дату рождения.",
        )
