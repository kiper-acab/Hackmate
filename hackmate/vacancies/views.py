__all__ = ()

import datetime

import django.contrib
import django.contrib.auth.mixins
import django.contrib.messages
import django.db
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.utils.timezone
import django.utils.translation
import django.views
import django.views.generic

import vacancies.forms
import vacancies.models


user_model = django.contrib.auth.get_user_model()


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
        return vacancies.models.Vacancy.objects.select_related(
            "creater",
            "creater__profile",
        ).filter(
            status=vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
            hackaton_date__gte=(
                django.utils.timezone.now() - datetime.timedelta(days=1)
            ),
        )[
            :10
        ]


class VacancyDetailView(
    django.views.generic.DetailView,
):
    model = vacancies.models.Vacancy
    template_name = "vacancies/detail.html"
    context_object_name = "vacancy"
    form_class = vacancies.forms.CommentForm

    def get_object(self):
        queryset = (
            self.get_queryset()
            .select_related("creater", "creater__profile")
            .prefetch_related(
                django.db.models.Prefetch(
                    "team_composition",
                    queryset=user_model.objects.select_related("profile"),
                ),
                "comments",
                django.db.models.Prefetch(
                    "comments__user",
                    queryset=user_model.objects.select_related("profile"),
                ),
            )
        )
        return django.shortcuts.get_object_or_404(
            queryset,
            pk=self.kwargs["pk"],
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        ip = get_client_ip(request)
        ip_instance, created = vacancies.models.Ip.objects.get_or_create(ip=ip)
        if not self.object.views.filter(ip=ip_instance).exists():
            self.object.views.add(ip_instance)

        return response  # noqa ругается falke на то что пресваиваю response, хотя по его мнению можно было избежать этого было, но для оптимизации запросы мы должны брать объект из self.object, а если мы

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return django.http.JsonResponse(
                {
                    "error": django.utils.translation.gettext_lazy(
                        "Вы должны быть авторизованы",
                    ),
                },
                status=403,
            )

        vacancy = self.get_object()

        form = vacancies.forms.CommentForm(request.POST) or None
        if form.is_valid():
            comment = form.save(commit=False)
            comment.vacancy = vacancy
            comment.user = request.user
            comment.save()
            return django.shortcuts.redirect(
                django.urls.reverse(
                    "vacancies:vacancy_detail",
                    kwargs={"pk": vacancy.pk},
                ),
            )

        if vacancies.models.Response.objects.filter(
            vacancy=vacancy,
            user=request.user,
            status__in=[
                "not_answered",
                "accepted",
            ],
        ).exists():
            return django.http.JsonResponse(
                {
                    "message": django.utils.translation.gettext_lazy(
                        "Вы уже откликнулись на эту вакансию",
                    ),
                },
            )

        vacancies.models.Response.objects.create(
            vacancy=vacancy,
            user=request.user,
        )

        return django.http.JsonResponse(
            {
                "message": django.utils.translation.gettext_lazy(
                    "Ваш отклик отправлен!",
                ),
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = vacancies.forms.CommentForm()
        return context


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


class UserResponsesView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "vacancies/user_responses.html"
    context_object_name = "responses"

    def get_queryset(self):
        return vacancies.models.Response.objects.filter(
            user=self.request.user,
            status__in=[
                vacancies.models.Response.ResponseStatuses.NOT_ANSWERED,
                vacancies.models.Response.ResponseStatuses.ACCEPTED,
            ],
        ).annotate(
            active_vacancy=django.db.models.FilteredRelation(
                "vacancy",
                condition=django.db.models.Q(
                    vacancy__status__in=[
                        vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
                        vacancies.models.Vacancy.VacancyStatuses.EQUIPPED,
                    ],
                    vacancy__hackaton_date__gte=(
                        django.utils.timezone.now()
                        - datetime.timedelta(days=1),
                    ),
                ),
            ),
        )


class UserVacanciesView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    model = vacancies.models.Vacancy
    template_name = "vacancies/user_vacancies.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        return vacancies.models.Vacancy.objects.filter(
            creater=self.request.user,
            status__in=[
                vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
                vacancies.models.Vacancy.VacancyStatuses.EQUIPPED,
            ],
        ).prefetch_related(
            django.db.models.Prefetch(
                "responses",
                queryset=vacancies.models.Response.objects.filter(
                    status=(
                        vacancies.models.Response.ResponseStatuses.NOT_ANSWERED
                    ),
                ),
            ),
        )


class CreateCommentView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    model = vacancies.models.CommentVacancy

    def get_success_url(self, requst, *args, **kwargs):
        return django.urls.reverse(
            "vacancies:vacancy_detail",
            args=[kwargs.get("pk")],
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        vacancy = vacancies.models.Vacancy.objects.get(pk=kwargs.get("pk"))
        comment = request.POST.get("comment")
        if comment:
            vacancies.models.CommentVacancy.objects.create(
                vacancy=vacancy,
                user=request.user,
                comment=comment,
            )

        return django.shortcuts.redirect(
            self.get_success_url(request, *args, **kwargs),
        )


class DeleteCommentView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DeleteView,
):
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

        if self.object.user == request.user or request.user.is_superuser:
            return super(DeleteCommentView, self).delete(
                request,
                *args,
                **kwargs,
            )

        raise django.http.Http404(
            django.utils.translation.gettext_lazy("not found"),
        )


class DeleteVacancy(django.views.generic.DeleteView):
    model = vacancies.models.Vacancy
    pk_url_kwarg = "pk"

    def get_success_url(self, *args, **kwargs):
        return django.urls.reverse(
            "vacancies:vacancies",
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.creater == request.user or request.user.is_superuser:
            self.object.status = (
                vacancies.models.Vacancy.VacancyStatuses.DELETED
            )
            self.object.save()
            return django.shortcuts.redirect(self.get_success_url())

        raise django.http.Http404(
            django.utils.translation.gettext_lazy("not found"),
        )


class ChangeVacancyView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    template_name = "vacancies/change_vacancy.html"
    form_class = vacancies.forms.VacancyForm
    model = vacancies.models.Vacancy
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        if (
            request.user != vacancy.creater
            or vacancy.status
            != vacancies.models.Vacancy.VacancyStatuses.ACTIVE
        ):
            raise django.http.Http404(
                django.utils.translation.gettext_lazy("not found"),
            )

        return super().get(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return django.urls.reverse(
            "vacancies:vacancy_detail",
            args=[self.get_object().pk],
        )


class AcceptInvite(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.BaseUpdateView,
):
    model = vacancies.models.Response
    success_url = django.urls.reverse_lazy("vacancies:user_vacancies")
    pk_url_kwargs = "pk"

    def get(self, request, *args, **kwargs):
        response = self.get_object()
        if (
            request.user == response.vacancy.creater
            and request.user != response.user
        ):
            response.vacancy.team_composition.add(response.user)
            response.status = (
                vacancies.models.Response.ResponseStatuses.ACCEPTED
            )
            response.save()

            response.vacancy.save()

            django.contrib.messages.success(
                request,
                django.utils.translation.gettext_lazy(
                    "Пользователь успешно приглашён в команду",
                ),
            )
            return django.shortcuts.redirect(self.success_url)

        return django.http.HttpResponseNotFound(
            django.utils.translation.gettext_lazy("not found"),
        )

    def get_queryset(self):
        return super().get_queryset().select_related("vacancy")


class RejectInvite(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.BaseDeleteView,
):
    model = vacancies.models.Response
    success_url = django.urls.reverse_lazy("vacancies:user_vacancies")
    pk_url_kwargs = "pk"

    def get(self, request, *args, **kwargs):
        response = self.get_object()
        if (
            request.user == response.vacancy.creater
            and request.user != response.user
            and response.vacancy.hackaton_date
            >= (
                django.utils.timezone.now() - datetime.timedelta(days=1)
            ).date()
        ):
            response.status = (
                vacancies.models.Response.ResponseStatuses.REJECTED
            )
            response.save()

            django.contrib.messages.success(
                request,
                django.utils.translation.gettext_lazy("Пользователь отклонён"),
            )

            return django.shortcuts.redirect(self.success_url)

        return django.http.HttpResponseNotFound(
            django.utils.translation.gettext_lazy("not found"),
        )


class KickUserFromVacancy(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.BaseDeleteView,
):
    model = vacancies.models.Vacancy
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        if (
            request.user == vacancy.creater
            and vacancy.status
            == vacancies.models.Vacancy.VacancyStatuses.ACTIVE
            and vacancy.hackaton_date
            >= (
                django.utils.timezone.now() - datetime.timedelta(days=1)
            ).date()
        ):
            user_id = kwargs.get("user_id")
            user = django.contrib.auth.get_user_model().objects.get(
                id=user_id,
            )
            vacancy.team_composition.remove(user)
            vacancy.save()

            django.contrib.messages.success(
                request,
                django.utils.translation.gettext_lazy(
                    f"Пользователь {user} удалён из команды",
                ),
            )

            return django.shortcuts.redirect(
                django.urls.reverse(
                    "vacancies:vacancy_detail",
                    args=[vacancy.pk],
                ),
            )

        return django.http.HttpResponseNotFound(
            django.utils.translation.gettext_lazy("not found"),
        )


class UserTeamsView(django.views.generic.ListView):
    template_name = "vacancies/my_teams.html"
    model = vacancies.models.Vacancy
    context_object_name = "teams"

    def get_queryset(self):
        return vacancies.models.Vacancy.objects.filter(
            django.db.models.Q(creater_id=self.request.user.pk)
            | django.db.models.Q(team_composition=self.request.user.pk),
        )
