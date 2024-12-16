import django.db.models.signals
import django.dispatch
import notifications.signals
import vacancies.models
import django.utils.translation

__all__ = ()


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
            description=django.utils.translation.gettext_lazy(
                "Пользователь {username} откликнулся на вакансию "
                "{vacancy_title}.",
            ).format(
                username=instance.user.username,
                vacancy_title=instance.vacancy.title,
            ),
        )
