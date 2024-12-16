__all__ = ()

import django.conf
import django.core.validators
import django.db.models
import django.utils.translation


class Ip(django.db.models.Model):
    ip = django.db.models.CharField(max_length=100)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy("IP адрес")
        verbose_name_plural = django.utils.translation.gettext_lazy(
            "IP адреса",
        )


class Vacancy(django.db.models.Model):
    class VacancyStatuses(django.db.models.TextChoices):
        ACTIVE = "active", "active"
        INACTIVE = "inactive", "inactive"

    creater = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name=django.utils.translation.gettext_lazy(
            "создатель вакансии",
        ),
    )

    title = django.db.models.CharField(
        max_length=255,
        verbose_name=django.utils.translation.gettext_lazy(
            "название вакансии",
        ),
    )

    description = django.db.models.TextField(
        verbose_name=django.utils.translation.gettext_lazy(
            "описание вакансии",
        ),
    )

    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name=django.utils.translation.gettext_lazy("создано"),
    )

    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name=django.utils.translation.gettext_lazy("обновлено"),
    )

    status = django.db.models.CharField(
        max_length=255,
        choices=VacancyStatuses.choices,
        verbose_name=django.utils.translation.gettext_lazy("cтатус"),
    )

    views = django.db.models.ManyToManyField(
        Ip,
        related_name="post_views",
        blank=True,
    )

    hackaton_title = django.db.models.CharField(
        max_length=255,
        verbose_name=django.utils.translation.gettext_lazy(
            "название хакатона",
        ),
        blank=True,
        null=True,
        help_text=django.utils.translation.gettext_lazy(
            "Название хакатона, к которому относится вакансия",
        ),
    )

    deadline = django.db.models.DateField(
        verbose_name=django.utils.translation.gettext_lazy("дедлайн"),
        null=True,
        blank=True,
        help_text=django.utils.translation.gettext_lazy(
            "Крайний срок подачи заявок",
        ),
    )

    required_experience = django.db.models.IntegerField(
        verbose_name=django.utils.translation.gettext_lazy(
            "требуемый опыт (в годах)",
        ),
        null=True,
        blank=True,
        help_text=django.utils.translation.gettext_lazy(
            "Укажите количество лет опыта, необходимого для кандидата",
        ),
        validators=[django.core.validators.MinValueValidator(0)],
    )

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy("вакансия")
        verbose_name_plural = django.utils.translation.gettext_lazy("вакансии")
        ordering = ["-created_at"]

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title


class CommentVacancy(django.db.models.Model):
    vacancy = django.db.models.ForeignKey(
        "Vacancy",
        on_delete=django.db.models.CASCADE,
        verbose_name=django.utils.translation.gettext_lazy("вакансия"),
        related_name="comments",
    )

    comment = django.db.models.TextField(
        verbose_name=django.utils.translation.gettext_lazy("комментарий"),
    )

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name=django.utils.translation.gettext_lazy("пользователь"),
    )

    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name=django.utils.translation.gettext_lazy("cоздано"),
    )

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy(
            "комментарий к вакансии",
        )
        verbose_name_plural = django.utils.translation.gettext_lazy(
            "комментарии к вакансиям",
        )
        ordering = ["-created_at"]


class Response(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name=django.utils.translation.gettext_lazy("пользователь"),
    )
    vacancy = django.db.models.ForeignKey(
        "Vacancy",
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name=django.utils.translation.gettext_lazy("вакансия"),
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name=django.utils.translation.gettext_lazy("дата отклика"),
    )

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy("отклик")
        verbose_name_plural = django.utils.translation.gettext_lazy("отклики")
        unique_together = (
            "user",
            "vacancy",
        )

    def __str__(self):
        return f"{self.user} -> {self.vacancy}"
