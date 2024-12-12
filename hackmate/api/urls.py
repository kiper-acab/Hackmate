import django.urls

import api.views


app_name = "api"

urlpatterns = [
    django.urls.path(
        "vacancies/",
        api.views.LoadMoreView.as_view(),
        name="vacancies",
    ),
]
