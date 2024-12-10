__all__ = ()

import django.conf
import django.db.models


class Ip(django.db.models.Model):
    ip = django.db.models.CharField(max_length=100)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "IP адрес"
        verbose_name_plural = "IP адреса"


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

    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="создано",
    )

    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name="обновлено",
    )

    status = django.db.models.CharField(
        max_length=255,
        choices=VacancyStatuses.choices,
        verbose_name="cтатус",
    )

    views = django.db.models.ManyToManyField(
        Ip,
        related_name="post_views",
        blank=True,
    )

    hackaton_title = django.db.models.CharField(
        max_length=255,
        verbose_name="название хакатона",
        blank=True,
        null=True,
        help_text="Название хакатона, к которому относится вакансия",
    )

    deadline = django.db.models.DateField(
        verbose_name="дедлайн",
        null=True,
        blank=True,
        help_text="Крайний срок подачи заявок",
    )

    required_experience = django.db.models.IntegerField(
        verbose_name="требуемый опыт (в годах)",
        null=True,
        blank=True,
        help_text="Укажите количество лет опыта, необходимого для кандидата",
    )

    class Meta:
        verbose_name = "вакансия"
        verbose_name_plural = "вакансии"

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title


class CommentVacancy(django.db.models.Model):
    vacancy = django.db.models.ForeignKey(
        "Vacancy",
        on_delete=django.db.models.CASCADE,
        verbose_name="вакансия",
        related_name="comments",
    )

    comment = django.db.models.TextField(
        verbose_name="комментарий",
    )

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )

    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="cоздано",
    )

    class Meta:
        verbose_name = "комментарий к вакансии"
        verbose_name_plural = "комментарии к вакансиям"
        ordering = ["-created_at"]


class Response(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name="Пользователь",
    )
    vacancy = django.db.models.ForeignKey(
        "Vacancy",
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name="Вакансия",
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отклика",
    )

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        unique_together = (
            "user",
            "vacancy",
        )

    def __str__(self):
        return f"{self.user} -> {self.vacancy}"
