__all__ = ()

import django.views.generic

import vacancies.models


class VacancyView(django.views.generic.ListView):
    template_name = "vacancies/vacancies.html"
    model = vacancies.models.Vacancy
    context_object_name = "vacancies"

    def get_queryset(self):
        return vacancies.models.Vacancy.objects.filter(
            status=vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
        )


class VacancyDetailView(django.views.generic.DetailView):
    model = vacancies.models.Vacancy
    template_name = "vacancies/detail.html"
    context_object_name = "vacancy"
