__all__ = []

import django.utils.deprecation

import users.models


class ProxyUserMiddleware(django.utils.deprecation.MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(pk=request.user.pk)

        return self.get_response(request)
