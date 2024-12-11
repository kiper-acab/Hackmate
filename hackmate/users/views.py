__all__ = []

import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.auth.models
import django.contrib.auth.views
import django.contrib.messages
import django.core.mail
import django.forms
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views
import django.views.generic

import users.forms
import users.models

User = django.contrib.auth.get_user_model()


class DeleteLinkView(django.views.generic.DeleteView):
    model = users.models.ProfileLink
    pk_url_kwarg = "pk"
    success_url = django.urls.reverse_lazy("users:profile_edit")

    def get_queryset(self):
        return super().get_queryset().select_related("profile__user")

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

        is_own_profile = user == request.user

        return django.shortcuts.render(
            request,
            "users/profile.html",
            {
                "user": user,
                "is_own_profile": is_own_profile,
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

        form = users.forms.UserChangeForm(instance=user)
        profile_form = users.forms.ProfileChangeForm(instance=user.profile)
        link_form = users.forms.ProfileLinkForm()
        links = users.models.ProfileLink.objects.filter(
            profile=request.user.profile,
        ).select_related("profile")

        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {
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

        form = users.forms.UserChangeForm(request.POST, instance=user)
        profile_form = users.forms.ProfileChangeForm(
            request.POST,
            request.FILES,
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

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save(commit=False)
            user_form.mail = users.models.UserManager().normalize_email(
                form.cleaned_data["email"],
            )

            if link_form.is_valid() and link_form.cleaned_data.get("url"):
                link = link_form.save(commit=False)
                link.profile = request.user.profile
                link.save()

            user_form.save()
            profile_form.save()
            django.contrib.messages.success(
                request,
                "Профиль успешно изменен!",
            )
            return django.shortcuts.redirect("users:profile_edit")

        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {
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
        user = django.shortcuts.get_object_or_404(User, username=username)

        if user.is_active:
            django.contrib.messages.error(
                request,
                "Пользователь уже активирован",
            )
            return django.shortcuts.redirect("users:login")

        if self.can_activate_user(user):
            user.is_active = True
            user.save()
            django.contrib.messages.success(
                request,
                "Пользователь успешно активирован",
            )
        else:
            django.contrib.messages.error(
                request,
                "Активация профиля была доступна в течение "
                f"{self.get_allowed_activation_time(user)} "
                "часов после регистрации",
            )

        return django.shortcuts.redirect("users:login")

    def can_activate_user(self, user):
        now = django.utils.timezone.now()
        time_difference = now - (
            user.profile.date_last_active or user.date_joined
        )
        allowed_hours = self.get_allowed_activation_time(user)
        return time_difference.total_seconds() // 3600 <= allowed_hours

    def get_allowed_activation_time(self, user):
        return 168 if user.profile.date_last_active else 12
