import django.urls

import api.views


app_name = "api"

urlpatterns = [
    django.urls.path(
        "vacancies/",
        api.views.LoadMoreVacacncies.as_view(),
        name="vacancies",
    ),
]
