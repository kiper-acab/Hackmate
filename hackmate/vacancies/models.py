__all__ = ()

import django.conf
import django.core.validators
import django.db.models
import django.utils.translation
import tinymce.models
import django.core.exceptions


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
        EQUIPPED = "equipped", "equipped"
        DELETED = "deleted", "deleted"

    class RequiredExperienceСhoices(django.db.models.TextChoices):
        NO_EXPIRIENCE = "no_expirience", django.utils.translation.gettext_lazy(
            "Нет опыта",
        )
        BIGGINER = "up_to_6_months", django.utils.translation.gettext_lazy(
            "До 6 месяцев",
        )
        MIDDLE = "6_to_12_months", django.utils.translation.gettext_lazy(
            "От 6 до 12 месяцев",
        )
        EXPERT = "more_than_12_months", django.utils.translation.gettext_lazy(
            "Более 1 года",
        )

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

    description = tinymce.models.HTMLField(
        verbose_name=django.utils.translation.gettext_lazy(
            "описание вакансии",
        ),
        validators=[
            django.core.validators.MinLengthValidator(
                5,
                django.utils.translation.gettext_lazy(
                    "Описание не может быть таким коротким",
                ),
            ),
            django.core.validators.MaxLengthValidator(
                10000,
                django.utils.translation.gettext_lazy(
                    "Описание не может быть таким длинным",
                ),
            ),
        ],
        help_text=django.utils.translation.gettext_lazy(
            "Описание вакансии должно быть от 5 до 10000 символов",
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

    hackaton_date = django.db.models.DateField(
        verbose_name=django.utils.translation.gettext_lazy(
            "Крайний срок подачи заявок",
        ),
        help_text=django.utils.translation.gettext_lazy(
            "Введите крайний срок подачи заявок",
        ),
    )

    required_experience = django.db.models.CharField(
        max_length=300,
        verbose_name=django.utils.translation.gettext_lazy("требуемый опыт"),
        help_text=django.utils.translation.gettext_lazy(
            "Укажите количество опыта необходимого для кандидата",
        ),
        choices=RequiredExperienceСhoices.choices,
        default=RequiredExperienceСhoices.NO_EXPIRIENCE,
    )

    team_composition = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        related_name="team_composition",
        verbose_name=django.utils.translation.gettext_lazy("состав команды"),
    )

    need_count_users = django.db.models.PositiveSmallIntegerField(
        verbose_name=(
            django.utils.translation.gettext_lazy(
                "необходимое количество человек "
                "в группе для участия в хакатоне",
            )
        ),
        validators=[
            django.core.validators.MinValueValidator(
                2,
                django.utils.translation.gettext_lazy(
                    "Введите корректное значение",
                ),
            ),
            django.core.validators.MaxValueValidator(
                100,
                django.utils.translation.gettext_lazy(
                    "Введите корректное значение",
                ),
            ),
        ],
    )

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy("вакансия")
        verbose_name_plural = django.utils.translation.gettext_lazy("вакансии")
        ordering = ["-created_at"]
        unique_together = ("title", "hackaton_title")

    def clean(self):
        if (
            Vacancy.objects.exclude(pk=self.pk)
            .filter(title=self.title, hackaton_title=self.hackaton_title)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                django.utils.translation.gettext_lazy(
                    "Вакансия с таким названием и хакатоном уже существует.",
                ),
            )

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
        validators=[
            django.core.validators.MinLengthValidator(
                5,
                django.utils.translation.gettext_lazy(
                    "Слишком короткий комментарий!",
                ),
            ),
            django.core.validators.MaxLengthValidator(
                3000,
                django.utils.translation.gettext_lazy(
                    "Комментарий не может привышать 3000 символов!",
                ),
            ),
        ],
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
    class ResponseStatuses(django.db.models.TextChoices):
        ACCEPTED = "accepted", "accepted"
        REJECTED = "rejected", "rejected"
        NOT_ANSWERED = "not_answered", "not_answered"

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name=django.utils.translation.gettext_lazy("пользователь"),
        unique=False,
    )
    vacancy = django.db.models.ForeignKey(
        "Vacancy",
        on_delete=django.db.models.CASCADE,
        related_name="responses",
        verbose_name=django.utils.translation.gettext_lazy("вакансия"),
        unique=False,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name=django.utils.translation.gettext_lazy("дата отклика"),
    )

    status = django.db.models.CharField(
        choices=ResponseStatuses.choices,
        max_length=255,
        default=ResponseStatuses.NOT_ANSWERED,
    )

    class Meta:
        verbose_name = django.utils.translation.gettext_lazy("отклик")
        verbose_name_plural = django.utils.translation.gettext_lazy("отклики")
        ordering = ["-created_at", "id"]

    def __str__(self):
        return f"{self.user} -> {self.vacancy}"
