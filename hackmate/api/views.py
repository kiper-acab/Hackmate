__all__ = ()

import django.core.cache
import django.http
import django.urls
import django.views.generic

import vacancies.models


class LoadMoreVacacncies(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 10))

        cache_key = f"vacancies_{offset}_{limit}"
        data = django.core.cache.cache.get(cache_key)

        if data is None:
            qs = vacancies.models.Vacancy.objects.select_related(
                "creater__profile",
            ).filter(status="active")
            # fmt: off
            vacancies_variable = qs[offset:offset + limit]
            # fmt: on
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
                        "profile_url": django.urls.reverse(
                            "users:profile",
                            args=[vacancy.creater.username],
                        ),
                    },
                    "deadline": (
                        vacancy.deadline.strftime("%Y-%m-%d")
                        if vacancy.deadline
                        else None
                    ),
                    "required_experience": vacancy.required_experience,
                    "vacancy_url": django.urls.reverse(
                        "vacancies:vacancy_detail",
                        args=[vacancy.pk],
                    ),
                }
                for vacancy in vacancies_variable
            ]
            django.core.cache.cache.set(cache_key, data, 3600)

        return django.http.JsonResponse(data, safe=False)


class LoadMoreComments(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs.get("pk")
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 10))

        vacancy_model = vacancies.models.CommentVacancy
        comments = (
            vacancy_model.objects.select_related(
                "user",
                "user__profile",
            )
            .filter(vacancy_id=vacancy_id)
            .order_by("-created_at")
            # fmt: off
            [offset:offset + limit]
            # fmt: on
        )

        data = [
            {
                "id": comment.id,
                "user": comment.user.username,
                "user_url": django.urls.reverse(
                    "users:profile",
                    args=[comment.user.username],
                ),
                "delete_url": django.urls.reverse(
                    "vacancies:delete_comment",
                    args=[comment.id],
                ),
                "comment": comment.comment,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                "current_user": request.user.username,
                "is_admin": request.user.is_superuser,
                "avatar": (
                    comment.user.profile.image.url
                    if comment.user.profile.image
                    else None
                ),
            }
            for comment in comments
        ]
        return django.http.JsonResponse(data, safe=False)
