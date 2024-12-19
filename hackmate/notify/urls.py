import django.urls

import notify.views


app_name = "notify"

urlpatterns = [
    django.urls.path(
        "readall_notifications/",
        notify.views.ReadAllNotificationsView.as_view(),
        name="readall_notifications",
    ),
    django.urls.path(
        "readone_notification/<int:pk>",
        notify.views.ReadOneNotificationView.as_view(),
        name="readone_notification",
    ),
]
