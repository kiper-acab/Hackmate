__all__ = []

import pathlib
import re
import sys

import django.conf
import django.contrib.auth.models
import django.db.models

import users.validators


class Country(django.db.models.Model):
    name = django.db.models.CharField(max_length=30, verbose_name="страна")

    def __str__(self):
        return self.name


class City(django.db.models.Model):
    country = django.db.models.ForeignKey(
        Country,
        on_delete=django.db.models.CASCADE,
    )
    name = django.db.models.CharField(max_length=30, verbose_name="город")

    def __str__(self):
        return self.name


if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    email_field = django.contrib.auth.models.User._meta.get_field("email")
    email_field._unique = True

    username_field = django.contrib.auth.models.User._meta.get_field(
        "username",
    )
    username_field._unique = True


def user_directory_path(instance, filename):
    username = instance.user.username
    return pathlib.Path("uploads") / "users_logos" / username / filename


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
        validators=[users.validators.validate_birthday],
    )

    image = django.db.models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
    )

    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
    )

    description = django.db.models.TextField(
        null=True,
        blank=True,
        verbose_name="о себе",
        help_text="Расскажите о себе",
    )
    country = django.db.models.ForeignKey(
        Country,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    city = django.db.models.ForeignKey(
        City,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )

    date_last_active = django.db.models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "дополнительная информация"
        verbose_name_plural = "дополнительные данные"


class ProfileLink(django.db.models.Model):
    SOCIAL_NETWORKS = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("vk", "VK"),
        ("gitlub", "GitLub"),
        ("github", "GitHub"),
    ]

    profile = django.db.models.ForeignKey(
        Profile,
        on_delete=django.db.models.CASCADE,
        related_name="links",
        verbose_name="профиль",
    )
    site_type = django.db.models.CharField(
        max_length=20,
        choices=SOCIAL_NETWORKS,
        verbose_name="тип сайта",
        null=True,
        blank=True,
    )
    url = django.db.models.URLField(
        verbose_name="URL",
        help_text="Полная ссылка, например, https://example.com",
        null=True,
        blank=True,
    )

    def get_fa_icon_class(self):
        fa_icons = {
            "facebook": "fa-facebook",
            "twitter": "fa-twitter",
            "instagram": "fa-instagram",
            "vk": "fa-vk",
            "gitlub": "fa-gitlab",
            "github": "fa-github",
        }
        return fa_icons.get(self.site_type, "fa-link")

    class Meta:
        verbose_name = "ссылка"
        verbose_name_plural = "ссылки"
