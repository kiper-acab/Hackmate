__all__ = []

import django.contrib.auth.models
import django.db.models.signals
import django.dispatch

import vacancies.models


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=vacancies.models.Vacancy,
)
def equippe_vacancy(sender, instance, created, **kwargs):
    if not created:
        if instance.team_composition.count() + 1 == instance.need_count_users:
            vacancies.models.Vacancy.objects.filter(id=instance.id).update(
                status=vacancies.models.Vacancy.VacancyStatuses.EQUIPPED,
            )
