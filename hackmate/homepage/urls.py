__all__ = ()

import django.urls

import homepage.views


app_name = "homepage"

urlpatterns = [
    django.urls.path(
        "",
        homepage.views.HomePageView.as_view(),
        name="homepage",
    ),
]
