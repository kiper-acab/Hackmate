import django.urls

import vacancies.views


app_name = "vacancies"

urlpatterns = [
    django.urls.path(
        "create/",
        vacancies.views.VacancyCreateView.as_view(),
        name="vacancy_create",
    ),
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
        "my-responses/",
        vacancies.views.UserResponsesView.as_view(),
        name="user_responses",
    ),
    django.urls.path(
        "my-vacancies/",
        vacancies.views.UserVacanciesView.as_view(),
        name="user_vacancies",
    ),
    django.urls.path(
        "delete_comment/<int:pk>/",
        vacancies.views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    django.urls.path(
        "delete_vacancy/<int:pk>/",
        vacancies.views.DeleteVacancy.as_view(),
        name="delete_vacancy",
    ),
]
