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


class ProfileView(
    django.views.generic.View,
    django.contrib.auth.mixins.LoginRequiredMixin,
):
    def get(self, request):
        form = users.forms.UserChangeForm(instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            instance=request.user.profile,
        )
        return django.shortcuts.render(
            request,
            "users/profile.html",
            {"form": form, "profile_form": profile_form},
        )


class ProfileEditView(
    django.views.generic.View,
    django.contrib.auth.mixins.LoginRequiredMixin,
):
    def get(self, request):
        form = users.forms.UserChangeForm(instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            instance=request.user.profile,
        )
        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {"form": form, "profile_form": profile_form},
        )

    def post(self, request):
        form = users.forms.UserChangeForm(request.POST, instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save(commit=False)
            user_form.mail = users.models.UserManager().normalize_email(
                form.cleaned_data["email"],
            )
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
            {"form": form, "profile_form": profile_form},
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
            confirmation_link = (
                "Чтобы подтвердить аккаунт перейдите по ссылке "
                f"http://127.0.0.1:8000{url}"
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
