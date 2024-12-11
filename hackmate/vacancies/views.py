__all__ = ()

import django.contrib
import django.contrib.auth.mixins
import django.core.paginator
import django.db.models
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
        return (
            vacancies.models.Vacancy.objects.filter(
                status=vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
            )
            .select_related("creater", "creater__profile")
            .prefetch_related("views", "comments__user")
        )


class VacancyDetailView(django.views.generic.DetailView):
    model = vacancies.models.Vacancy
    template_name = "vacancies/detail.html"
    context_object_name = "vacancy"
    form_class = vacancies.forms.CommentForm

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "creater",
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    "views",
                    queryset=vacancies.models.Ip.objects.only(
                        "id",
                        "ip",
                    ),
                ),
            )
            .annotate(
                view_count=django.db.models.Count(
                    "views",
                    distinct=True,
                ),
            )
        )

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        ip = get_client_ip(request)

        ip_views_queryset = vacancy.views.only("id", "ip")
        view_exists = ip_views_queryset.filter(ip=ip).exists()
        if not view_exists:
            vacancy.views.create(ip=ip)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()

        if not request.user.is_authenticated:
            return django.http.JsonResponse(
                {
                    "error": "Вы должны быть авторизованы "
                    "для выполнения этого действия",
                },
                status=403,
            )

        if "comment" in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.instance.vacancy = vacancy
                form.instance.user = request.user
                form.save()
                return django.http.JsonResponse(
                    {"message": "Комментарий добавлен!"},
                )

            return django.http.JsonResponse(
                {"error": "Форма комментария недействительна."},
                status=400,
            )

        response, created = vacancies.models.Response.objects.get_or_create(
            vacancy=vacancy,
            user=request.user,
        )

        if not created:
            return django.http.JsonResponse(
                {"message": "Вы уже откликнулись на эту вакансию."},
            )

        return django.http.JsonResponse(
            {"message": "Ваш отклик успешно отправлен!"},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.object

        context.update(
            {
                "comment_form": self.form_class(),
                "is_deadline_passed": vacancy.deadline
                and vacancy.deadline < django.utils.timezone.now().date(),
                "comments": vacancy.comments.all(),
                "view_count": vacancy.view_count,
                "similar_vacancies": self.get_similar_vacancies(vacancy),
            },
        )
        return context

    def get_similar_vacancies(self, vacancy):
        return (
            self.model.objects.filter(
                status=self.model.VacancyStatuses.ACTIVE,
                hackaton_title=vacancy.hackaton_title,
            )
            .exclude(id=vacancy.id)
            .select_related("creater")[:5]
        )


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
        ).select_related(
            "vacancy",
            "vacancy__creater",
        )


class UserVacanciesView(django.views.generic.ListView):
    model = vacancies.models.Vacancy
    template_name = "vacancies/user_vacancies.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        return vacancies.models.Vacancy.objects.filter(
            creater=self.request.user,
        ).prefetch_related(
            "responses",
            "responses__user",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginated_responses = {}
        for vacancy in context["vacancies"]:
            responses = vacancy.responses.all()
            paginator = django.core.paginator.Paginator(responses, 5)
            page_number = self.request.GET.get(f"page_{vacancy.id}", 1)
            paginated_responses[vacancy.id] = paginator.get_page(page_number)

        context["paginated_responses"] = paginated_responses
        return context


class DeleteCommentView(django.views.generic.DeleteView):
    model = vacancies.models.CommentVacancy
    pk_url_kwarg = "pk"
    template_name = "vacancies/user_vacancies.html"

    def get_success_url(self, *args, **kwargs):
        return django.urls.reverse(
            "vacancies:vacancy_detail",
            args=[self.object.vacancy.pk],
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user == request.user:
            return super(DeleteCommentView, self).delete(
                request,
                *args,
                **kwargs,
            )

        raise django.http.Http404("not found")
