__all__ = ()

import django.contrib
import django.contrib.auth.mixins
import django.http
import django.shortcuts
import django.urls
import django.views.generic
import notifications.models


class ReadAllNotificationsView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def get(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_read()
        return django.shortcuts.redirect(
            django.urls.reverse("homepage:homepage"),
        )


class ReadOneNotificationView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    model = notifications.models.Notification

    def get(self, request, *args, **kwargs):
        notification = django.shortcuts.get_object_or_404(
            notifications.models.Notification,
            pk=kwargs.get("pk"),
            recipient=request.user,
        )
        notification.mark_as_read()

        return django.shortcuts.redirect(
            django.urls.reverse("homepage:homepage"),
        )
