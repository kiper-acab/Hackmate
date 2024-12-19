__all__ = ()

import django.views.generic


class AboutPageView(django.views.generic.TemplateView):
    template_name = "about/about.html"


class PrivacyPageView(django.views.generic.TemplateView):
    template_name = "about/privacy.html"


class ContactPageView(django.views.generic.TemplateView):
    template_name = "about/contact.html"
