import django.urls

import vacancies.views


app_name = "vacancies"

urlpatterns = [
    django.urls.path(
        "",
        vacancies.views.VacancyView.as_view(),
        name="vacancies",
    ),
    django.urls.path(
        "<int:pk>/",
        vacancies.views.VacancyDetailView.as_view(),
        name="vacancy_detail",
    ),
    django.urls.path(
        "my-vacancies/",
        vacancies.views.UserVacanciesView.as_view(),
        name="user_vacancies",
    ),
    django.urls.path(
        "create/",
        vacancies.views.VacancyCreateView.as_view(),
        name="vacancy_create",
    ),
    django.urls.path(
        "delete_vacancy/<int:pk>/",
        vacancies.views.DeleteVacancy.as_view(),
        name="delete_vacancy",
    ),
    django.urls.path(
        "my-responses/",
        vacancies.views.UserResponsesView.as_view(),
        name="user_responses",
    ),
    django.urls.path(
        "delete_comment/<int:pk>/",
        vacancies.views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    django.urls.path(
        "create_comment/<int:pk>/",
        vacancies.views.CreateCommentView.as_view(),
        name="create_comment",
    ),
    django.urls.path(
        "change_vacancy/<int:pk>/",
        vacancies.views.ChangeVacancyView.as_view(),
        name="change_vacancy",
    ),
    django.urls.path(
        "invite_user/<int:pk>/",
        vacancies.views.AcceptInvite.as_view(),
        name="invite_user",
    ),
    django.urls.path(
        "reject_user/<int:pk>/",
        vacancies.views.RejectInvite.as_view(),
        name="reject_user",
    ),
    django.urls.path(
        "kick_user/<int:pk>/<int:user_id>/",
        vacancies.views.KickUserFromVacancy.as_view(),
        name="kick_user",
    ),
]
