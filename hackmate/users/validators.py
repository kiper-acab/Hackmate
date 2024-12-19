__all__ = ()

import datetime

import django.core.exceptions
import django.utils.timezone
import django.utils.translation


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


class MaximumLengthValidator:
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise django.core.exceptions.ValidationError(
                django.utils.translation.gettext(
                    "Пароль может содержать максимум %(max_length)d символов.",
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return django.utils.translation.gettext(
            "Пароль может содержать максимум %(max_length)d символов."
            % {"max_length": self.max_length},
        )


def validate_social_network_url(value, site_type):
    expected_prefixes = {
        "facebook": "https://facebook.com/",
        "twitter": "https://x.com/",
        "instagram": "https://www.instagram.com/",
        "vk": "https://vk.com/",
        "gitlab": "https://gitlab",
        "github": "https://github.com/",
    }

    if site_type not in expected_prefixes:
        raise django.core.exceptions.ValidationError(
            f"Неизвестный тип сайта: {site_type}",
        )

    expected_prefix = expected_prefixes[site_type]
    if not value.startswith(expected_prefix):
        raise django.core.exceptions.ValidationError(
            f"Ссылка должна начинаться с '{expected_prefix}'.Текущий: {value}",
        )
