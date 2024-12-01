__all__ = ()

import datetime

import django.core.exceptions
import django.utils.timezone


def validate_birthday(value):
    today = django.utils.timezone.now().date()
    oldest_allowed = today - datetime.timedelta(days=150 * 365)
    if value > today:
        raise django.core.exceptions.ValidationError(
            "Дата рождения не может быть в будущем.",
        )

    if value < oldest_allowed:
        raise django.core.exceptions.ValidationError(
            "Дата рождения не может быть более 150 лет назад.",
        )
