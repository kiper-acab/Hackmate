__all__ = ()

import django.views.generic

import vacancies.models


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]

    return request.META.get("REMOTE_ADDR")


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

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        ip = get_client_ip(request)
        ip_instance, created = vacancies.models.Ip.objects.get_or_create(ip=ip)
        vacancy.views.add(ip_instance)

        return super().get(request, *args, **kwargs)
