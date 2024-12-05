import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.urls


main_urlpatterns = [
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("auth/", django.urls.include("users.urls")),
    django.urls.path("vacancy/", django.urls.include("vacancies.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("chaining/", django.urls.include("smart_selects.urls")),
]

static_urlpatterns = django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)

urlpatterns = main_urlpatterns + static_urlpatterns

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    ]
