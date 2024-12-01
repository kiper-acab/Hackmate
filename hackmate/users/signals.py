__all__ = []

import django.contrib.auth.models
import django.db.models.signals
import django.dispatch

import users.models


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=django.contrib.auth.models.User,
)
@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=users.models.User,
)
def add_users_profile(sender, instance, created, **kwargs):
    if created:
        users.models.Profile.objects.get_or_create(user=instance)
