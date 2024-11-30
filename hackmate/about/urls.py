__all__ = ()

import django.urls

import about.views


app_name = "about"

urlpatterns = [
    django.urls.path(
        "",
        about.views.AboutPageView.as_view(),
        name="about",
    ),
    django.urls.path(
        "contact/",
        about.views.ContactPageView.as_view(),
        name="contact",
    ),
    django.urls.path(
        "privacy/",
        about.views.PrivacyPageView.as_view(),
        name="privacy",
    ),
]
