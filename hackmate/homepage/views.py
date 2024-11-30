__all__ = ()

import django.views.generic


class HomePageView(django.views.generic.TemplateView):
    template_name = "homepage/homepage.html"
