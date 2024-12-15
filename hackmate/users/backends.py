__all__ = ()

import django.conf
import django.contrib.auth.backends
import django.contrib.auth.models
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone

import users.models


class EmailOrUsernameModelBackend(django.contrib.auth.backends.BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        if "@" in username:
            user = users.models.User.objects.by_mail(username)
        else:
            user = users.models.User.objects.filter(username=username).first()

        if user:
            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            if (
                user.profile.attempts_count
                < django.conf.settings.MAX_AUTH_ATTEMPTS - 1
                and user.is_active
            ):
                django.contrib.messages.error(
                    request,
                    (
                        "Неправильный логин/пароль. "
                        "Убедитесь в корректности данных."
                    ),
                )
                user.profile.attempts_count += 1
                user.profile.save()

            else:
                self.deactivate_user(request, user)

        else:
            django.contrib.messages.error(
                request,
                "Пользователь с таким логином/почтой не найден.",
            )

        return None

    def deactivate_user(self, request, user):
        now = django.utils.timezone.now()
        user = users.models.User.objects.filter(pk=user.pk).first()
        user.profile.attempts_count = 0
        user.profile.date_last_active = now

        user.profile.save()

        django.contrib.messages.error(
            request,
            (
                "Вы превысили допустимое число попыток входа. "
                "Пожалуйста, активируйте свой аккаунт. "
                "Вам должно прийти письмо на почту с активацией."
            ),
        )

        if user.is_active:
            activation_path = django.urls.reverse(
                "users:activate",
                args=[user.username],
            )
            domain = request.get_host()
            confirmation_link = (
                "Замечена подозрительная активность аккаунта. "
                "Для активации аккаунта нажмите на ссылку ниже: "
                f"http://{domain}{activation_path}"
            )

            django.core.mail.send_mail(
                "Активация аккаунта",
                confirmation_link,
                django.conf.settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        user.is_active = False
        user.save()

    def get_user(self, user_id):
        queryset = django.contrib.auth.models.User.objects.select_related(
            "profile",
        )
        return queryset.filter(pk=user_id).first()
