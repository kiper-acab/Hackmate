__all__ = ()

import django.db.models.signals
import django.dispatch
import notifications.signals

import vacancies.models


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=vacancies.models.Response,
)
def add_notification(sender, instance, created, **kwargs):
    if created:
        notifications.signals.notify.send(
            instance.user,
            recipient=instance.vacancy.creater,
            verb="оставил отклик на вашу вакансию",
            description=(
                f"Пользователь {instance.user.username}"
                f"откликнулся на вакансию {instance.vacancy.title}."
            ),
        )