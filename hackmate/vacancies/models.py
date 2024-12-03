__all__ = ()

import django.conf
import django.db.models


class Ip(django.db.models.Model):
    ip = django.db.models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Vacancy(django.db.models.Model):
    class VacancyStatuses(django.db.models.TextChoices):
        ACTIVE = "active", "active"
        FINISHED = "finished", "finished"

    creater = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="создатель вакансии",
    )

    title = django.db.models.CharField(
        max_length=255,
        verbose_name="название вакансии",
    )

    description = django.db.models.TextField(verbose_name="описание вакансии")

    created_at = django.db.models.DateTimeField(auto_now_add=True)

    updated_at = django.db.models.DateTimeField(auto_now=True)

    status = django.db.models.CharField(
        max_length=255,
        choices=VacancyStatuses.choices,
    )

    views = django.db.models.ManyToManyField(
        Ip,
        related_name="post_views",
        blank=True,
    )

    def total_views(self):
        return self.views.count()

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"
