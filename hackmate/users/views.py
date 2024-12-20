__all__ = []

import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.auth.models
import django.contrib.auth.views
import django.contrib.messages
import django.core.exceptions
import django.core.mail
import django.forms
import django.http
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views
import django.views.generic
import star_ratings.models

import users.forms
import users.models
import vacancies.models

User = django.contrib.auth.get_user_model()


class DeleteLinkView(django.views.generic.DeleteView):
    model = users.models.ProfileLink
    pk_url_kwarg = "pk"
    success_url = django.urls.reverse_lazy("users:profile_edit")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.profile.user != request.user:
            django.contrib.messages.error(
                request,
                "Вы не можете удалить эту ссылку.",
            )
            return django.shortcuts.redirect(self.success_url)

        self.object.delete()
        return django.shortcuts.redirect(self.success_url)


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):

    def get(self, request, username):
        user = django.shortcuts.get_object_or_404(
            users.models.User.objects.select_related("profile"),
            username=username,
        )
        finished_vacancies = (
            vacancies.models.Vacancy.objects.filter(
                creater_id=user.id,
                status=vacancies.models.Vacancy.VacancyStatuses.FINISHED,
            )
            .select_related("creater")
            .prefetch_related("responses")
        )

        is_own_profile = user == request.user
        try:
            rating_user = star_ratings.models.Rating.objects.get(
                object_id=user.id,
            )
        except django.core.exceptions.ObjectDoesNotExist:
            rating_user = star_ratings.models.Rating.objects.create(
                content_object=user,
            )

        return django.shortcuts.render(
            request,
            "users/profile.html",
            {
                "user": user,
                "is_own_profile": is_own_profile,
                "rating_count": rating_user,
                "finished_vacancies": finished_vacancies,
            },
        )


class ProfileEditView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):

    def get(self, request):
        user = users.models.User.objects.select_related("profile").get(
            pk=request.user.pk,
        )
        image_form = users.forms.ProfileImageChangeForm(instance=user.profile)
        form = users.forms.UserChangeForm(instance=user)
        profile_form = users.forms.ProfileChangeForm(instance=user.profile)
        link_form = users.forms.ProfileLinkForm()
        links = users.models.ProfileLink.objects.filter(
            profile=user.profile,
        ).select_related("profile")

        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {
                "image_form": image_form,
                "form": form,
                "profile_form": profile_form,
                "link_form": link_form,
                "links": links,
            },
        )

    def post(self, request):
        user = users.models.User.objects.select_related("profile").get(
            pk=request.user.pk,
        )
        image_form = users.forms.ProfileImageChangeForm(
            request.POST,
            request.FILES,
            instance=user.profile,
        )
        form = users.forms.UserChangeForm(request.POST, instance=user)
        profile_form = users.forms.ProfileChangeForm(
            request.POST,
            instance=user.profile,
        )
        link_form = users.forms.ProfileLinkForm(request.POST)

        if not form.data.get("email") or not form.data.get("username"):
            django.contrib.messages.error(
                request,
                "Поля Email и Username обязательны для заполнения.",
            )
            return django.shortcuts.render(
                request,
                "users/profile_edit.html",
                {"form": form, "profile_form": profile_form},
            )

        if "delete_image" in request.POST:
            user.profile.image.delete()
            user.profile.image = None
            user.profile.save()
            django.contrib.messages.success(
                request,
                "Изображение профиля успешно удалено.",
            )
            return django.shortcuts.redirect(
                django.urls.reverse_lazy("users:profile_edit"),
            )

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save(commit=False)
            user_form.email = users.models.UserManager().normalize_email(
                form.cleaned_data["email"],
            )

            if link_form.is_valid() and link_form.cleaned_data.get("url"):
                link = link_form.save(commit=False)
                link.profile = user.profile
                link.save()

            user_form.save()
            profile_form.save()
            image_form.save()
            django.contrib.messages.success(
                request,
                "Профиль успешно изменен!",
            )
            return django.shortcuts.redirect(
                "users:profile_edit",
            )

        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {
                "image_form": image_form,
                "form": form,
                "profile_form": profile_form,
                "link_form": link_form,
            },
        )


class SignUpView(
    django.views.generic.FormView,
):
    template_name = "users/signup.html"
    form_class = users.forms.UserCreateForm
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = users.models.UserManager().normalize_email(
            form.cleaned_data["email"],
        )
        user.set_password(form.cleaned_data["password1"])

        if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
            user.is_active = True
        else:
            user.is_active = False
            url = django.urls.reverse("users:activate", args=[user.username])
            domain = self.request.get_host()
            confirmation_link = (
                "Чтобы подтвердить аккаунт перейдите по ссылке "
                f"http://{domain}{url}"
            )

            django.core.mail.send_mail(
                "Activate your account",
                confirmation_link,
                django.conf.settings.DJANGO_MAIL,
                [user.email],
                fail_silently=False,
            )

        user.save()

        django.contrib.messages.success(
            self.request,
            "Пользователь успешно создан",
        )
        django.contrib.messages.info(
            self.request,
            "Активируйте профиль в письме, которое придет вам на почту",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ActivateUserView(django.views.View):
    def get(self, request, username):
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.models.User,
            username=username,
        )
        now = django.utils.timezone.now()

        if not user.profile.date_last_active:
            time_difference = now - user.date_joined
            allowed_activation_time = 12
        else:
            time_difference = now - user.profile.date_last_active
            allowed_activation_time = 168

        datediff = int(time_difference.total_seconds() // 3600)

        if not user.is_active:
            if datediff <= allowed_activation_time:
                user.is_active = True
                user.profile.save()
                user.save()
                django.contrib.messages.success(
                    request,
                    ("Пользователь успешно активирован"),
                )
            else:
                django.contrib.messages.error(
                    request,
                    (
                        "Активация профиля была "
                        "доступна в течение {allowed_activation_time} "
                        "часов после регистрации"
                    ),
                )
        else:
            django.contrib.messages.error(
                request,
                ("Пользователь уже активирован"),
            )

        return django.shortcuts.redirect(django.urls.reverse("users:login"))


class CustomPasswordResetCompleteView(
    django.contrib.auth.views.PasswordResetCompleteView,
):
    template_name = "users/password_reset_confirm.html"
    form_class = users.forms.PasswordResetCompleteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data["feedback"]
            print(f"Отзыв получен: {feedback}")
            return django.http.HttpResponseRedirect(
                django.urls.reverse_lazy("users:password_reset_complete"),
            )

        return django.shortcuts.render(
            request,
            self.template_name,
            {"form": form},
        )
