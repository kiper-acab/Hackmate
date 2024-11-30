__all__ = ()

import django.conf
import django.contrib.auth.backends
import django.contrib.auth.models
import django.contrib.messages
import django.shortcuts
import django.urls
import django.utils.timezone

import users.models


class EmailOrUsernameModelBackend(django.contrib.auth.backends.BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if "@" in username:
            user = users.models.User.objects.by_mail(username) or None

        else:
            user = (
                users.models.User.objects.filter(username=username).first()
                or None
            )

        if user and user.check_password(password):
            return user

        return None
