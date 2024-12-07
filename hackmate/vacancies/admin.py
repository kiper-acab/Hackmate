__all__ = ()

import django.contrib.admin

import vacancies.models


@django.contrib.admin.register(vacancies.models.Vacancy)
class UserInfoAdmin(django.contrib.admin.ModelAdmin):

    list_display = (
        vacancies.models.Vacancy.creater.field.name,
        vacancies.models.Vacancy.title.field.name,
        vacancies.models.Vacancy.status.field.name,
    )


django.contrib.admin.site.register(vacancies.models.Ip)
django.contrib.admin.site.register(vacancies.models.CommentVacancy)
