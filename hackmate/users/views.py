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

        user.is_active = False
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
    pass
