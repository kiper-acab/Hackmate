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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.profile.user != request.user:
            django.contrib.messages.error(
                request,
                "Вы не можете удалить эту ссылку.",
            )
            return django.shortcuts.redirect(self.success_url)

        self.object.delete()
        success_url = django.urls.reverse(
            "users:profile_edit",
            args=[self.object.link.pk],
        )
        return django.shortcuts.redirect(success_url)


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def get(self, request):
        form = users.forms.UserChangeForm(instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            instance=request.user.profile,
        )
        link_form = users.forms.ProfileLinkForm()

        return django.shortcuts.render(
            request,
            "users/profile.html",
            {
                "form": form,
                "profile_form": profile_form,
                "link_form": link_form,
            },
        )


class ProfileEditView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def get(self, request):
        form = users.forms.UserChangeForm(instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            instance=request.user.profile,
        )
        link_form = users.forms.ProfileLinkForm()
        links = users.models.ProfileLink.objects.filter(
            profile=request.user.profile,
        )
        country_form = users.forms.CountryFrom(
            instance=request.user.profile,
        )
        city_form = users.forms.CityFrom(
            instance=request.user.profile,
        )

        return django.shortcuts.render(
            request,
            "users/profile_edit.html",
            {
                "form": form,
                "profile_form": profile_form,
                "link_form": link_form,
                "links": links,
                "country_form": country_form,
                "city_form": city_form,
            },
        )

    def post(self, request):
        form = users.forms.UserChangeForm(request.POST, instance=request.user)
        profile_form = users.forms.ProfileChangeForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )
        link_form = users.forms.ProfileLinkForm(request.POST)
        country_form = users.forms.CountryFrom(
            request.POST, instance=request.user.profile,
        )
        city_form = users.forms.CityFrom(
            request.POST, instance=request.user.profile,
        )

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

            if country_form.is_valid():
                country_form.save()

            if city_form.is_valid():
                city_form.save()

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
                "country_form": country_form,
                "city_form": city_form,
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
