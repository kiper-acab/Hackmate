__all__ = ()

import django.db.models
import django.utils.deprecation
import notifications.models

import users.models


class ProxyUserMiddleware(django.utils.deprecation.MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            notifications_queryset = (
                notifications.models.Notification.objects.filter(
                    recipient=request.user,
                ).only("id", "actor", "verb", "timestamp", "unread")
            )
            request.user = (
                users.models.User.objects.prefetch_related(
                    django.db.models.Prefetch(
                        "notifications",
                        queryset=notifications_queryset,
                    ),
                )
                .select_related("profile")
                .get(pk=request.user.pk)
            )

        return self.get_response(request)
