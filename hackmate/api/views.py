__all__ = ()

import django.core.cache
import django.http
import django.views.generic

import vacancies.models


class LoadMoreView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 10))

        cache_key = f"vacancies_{offset}_{limit}"
        data = django.core.cache.cache.get(cache_key)

        if data is None:
            vacancies_variable = (
                vacancies.models.Vacancy.objects.select_related(
                    "creater__profile",
                ).filter(status="active")[
                    offset : offset + limit  # noqa Flake8: E203
                ]
                # noqa конфликт black и flake8
            )
            data = [
                {
                    "id": vacancy.id,
                    "title": vacancy.title,
                    "description": vacancy.description,
                    "creater": {
                        "username": vacancy.creater.username,
                        "profile_image": (
                            vacancy.creater.profile.image.url
                            if vacancy.creater.profile.image
                            else None
                        ),
                    },
                    "deadline": (
                        vacancy.deadline.strftime("%Y-%m-%d")
                        if vacancy.deadline
                        else None
                    ),
                    "required_experience": vacancy.required_experience,
                }
                for vacancy in vacancies_variable
            ]
            django.core.cache.cache.set(cache_key, data, 3600)

        return django.http.JsonResponse(data, safe=False)
