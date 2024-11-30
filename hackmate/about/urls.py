__all__ = ()

import about.views
import django.urls


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
