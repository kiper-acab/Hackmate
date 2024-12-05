__all__ = ()

import django.contrib
import django.contrib.auth.mixins
import django.http
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import vacancies.forms
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

        ip = self.get_client_ip(request)
        ip_instance, created = vacancies.models.Ip.objects.get_or_create(ip=ip)
        if not vacancy.views.filter(ip=ip_instance).exists():
            vacancy.views.add(ip_instance)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return django.http.JsonResponse(
                {"error": "Вы должны быть авторизованы"},
                status=403,
            )

        vacancy = self.get_object()

        if vacancies.models.Response.objects.filter(
            vacancy=vacancy,
            user=request.user,
        ).exists():
            return django.http.JsonResponse(
                {"message": "Вы уже откликнулись на эту вакансию"},
            )

        vacancies.models.Response.objects.create(
            vacancy=vacancy,
            user=request.user,
        )

        return django.http.JsonResponse({"message": "Ваш отклик отправлен!"})

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]

        return request.META.get("REMOTE_ADDR")


class VacancyCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    model = vacancies.models.Vacancy
    form_class = vacancies.forms.VacancyForm
    template_name = "vacancies/vacancy_form.html"
    success_url = django.urls.reverse_lazy("vacancies:vacancies")

    def form_valid(self, form):
        form.instance.creater = self.request.user
        form.instance.status = vacancies.models.Vacancy.VacancyStatuses.ACTIVE
        return super().form_valid(form)


class UserResponsesView(django.views.generic.ListView):
    template_name = "vacancies/user_responses.html"
    context_object_name = "responses"

    def get_queryset(self):
        return vacancies.models.Response.objects.filter(
            user=self.request.user,
        ).select_related("vacancy")


class UserVacanciesView(django.views.generic.ListView):
    model = vacancies.models.Vacancy
    template_name = "vacancies/user_vacancies.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        return vacancies.models.Vacancy.objects.filter(
            creater=self.request.user,
        ).prefetch_related("responses")