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
                "Форма успешно отправлена!",
            )
            return django.shortcuts.redirect("users:profile")

        return django.shortcuts.render(
            request,
            "users/profile.html",
            {"form": form, "profile_form": profile_form},
        )


class SignUpView(
    django.views.generic.FormView,
):
    pass


class ActivateUserView(django.views.View):
    pass
