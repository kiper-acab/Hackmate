__all__ = []


import re
import sys

import django.conf
import django.contrib.auth.models
import django.db.models

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    email_field = django.contrib.auth.models.User._meta.get_field("email")
    email_field._unique = True

    username_field = django.contrib.auth.models.User._meta.get_field(
        "username",
    )
    username_field._unique = True


class UserManager(django.contrib.auth.models.UserManager):
    def normalize_email(self, email):
        email = super().normalize_email(email)
        email = email.lower()
        local_part, domain = email.split("@")

        local_part = local_part.split("+")[0]

        if domain in ["yandex.ru", "ya.ru"]:
            domain = "yandex.ru"
            local_part = local_part.replace(".", "-")
        elif domain == "gmail.com":
            local_part = local_part.replace(".", "")

        local_part = re.sub(r"\+.*", "", local_part)
        return f"{local_part}@{domain}"

    def active(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .select_related("profile")
        )

    def inactive(self):
        return (
            self.get_queryset()
            .filter(is_active=False)
            .select_related("profile")
        )

    def by_mail(self, identifier):
        normalized_email = self.normalize_email(identifier)
        return self.active().filter(email=normalized_email).first() or None


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
    )

    birthday = django.db.models.DateField(
        null=True,
        blank=True,
        verbose_name="день рождения",
        help_text="Введите дату рождения",
    )

    image = django.db.models.ImageField(
        upload_to="uploads/profile",
        null=True,
        blank=True,
    )

    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
    )

    description = django.db.models.TextField(null=True, blank=True)

    date_last_active = django.db.models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "дополнительная информация"
        verbose_name_plural = "дополнительные данные"
