__all__ = ()

import django.db.models.signals
import django.dispatch
import django.utils.translation
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
            verb=django.utils.translation.gettext_lazy(
                "оставил отклик на вашу вакансию",
            ),
            description=(
                django.utils.translation.gettext_lazy(
                    f"Пользователь {instance.user.username}"
                    f"откликнулся на вакансию {instance.vacancy.title}.",
                )
            ),
        )
    else:
        if (
            instance.status
            == vacancies.models.Response.ResponseStatuses.ACCEPTED
        ):
            notifications.signals.notify.send(
                instance.vacancy.creater,
                recipient=instance.user,
                verb=django.utils.translation.gettext_lazy(
                    "принял вас в команду",
                ),
                description=(
                    django.utils.translation.gettext_lazy(
                        f"Пользователь {instance.user.username}"
                        f"принял вас в команду.",
                    )
                ),
            )
        elif (
            instance.status
            == vacancies.models.Response.ResponseStatuses.REJECTED
        ):
            notifications.signals.notify.send(
                instance.vacancy.creater,
                recipient=instance.user,
                verb=django.utils.translation.gettext_lazy(
                    "отклонил ваш отклик",
                ),
                description=(
                    django.utils.translation.gettext_lazy(
                        f"Пользователь {instance.user.username}"
                        f"отклонил ваш отклик.",
                    )
                ),
            )
