__all__ = []

import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms
import django.utils.translation

import users.models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class UserChangeForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.required = True

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            model.email.field.name,
            model.username.field.name,
        )


class UserCreateForm(
    django.contrib.auth.forms.UserCreationForm,
    BootstrapForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        namefield = django.contrib.auth.models.User.email.field.name
        self.fields[namefield].required = True

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        fields = (
            UserChangeForm.Meta.model.email.field.name,
            UserChangeForm.Meta.model.username.field.name,
            "password1",
            "password2",
        )

        labels = {
            UserChangeForm.Meta.model.username.field.name: (
                django.utils.translation.gettext_lazy("Введите логин")
            ),
        }


class ProfileChangeForm(BootstrapForm):
    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
            users.models.Profile.description.field.name,
        )

        labels = {
            users.models.Profile.image.field.name: (
                django.utils.translation.gettext_lazy("Выберите себе картинку")
            ),
            users.models.Profile.description.field.name: (
                django.utils.translation.gettext_lazy("Описание")
            ),
        }

        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={"type": "date"},
                format=("%Y-%m-%d"),
            ),
            users.models.Profile.image.field.name: django.forms.FileInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.data.get("delete_image"):
            instance.image.delete(save=False)
            instance.image = None

        if commit:
            instance.save()

        return instance


class ProfileLinkForm(BootstrapForm):
    class Meta:
        model = users.models.ProfileLink
        fields = [
            users.models.ProfileLink.site_type.field.name,
            users.models.ProfileLink.url.field.name,
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[users.models.ProfileLink.site_type.field.name].label = (
            django.utils.translation.gettext_lazy("Тип сайта")
        )
        self.fields[users.models.ProfileLink.url.field.name].label = (
            django.utils.translation.gettext_lazy("Ссылка")
        )
        self.fields[users.models.ProfileLink.site_type.field.name].required = (
            False
        )
        self.fields[users.models.ProfileLink.url.field.name].required = False


class AuthenticateForm(
    django.contrib.auth.forms.AuthenticationForm,
    BootstrapForm,
):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["password"].widget.label = (
            django.utils.translation.gettext_lazy("Пароль")
        )

    username = django.forms.CharField(
        label=django.utils.translation.gettext_lazy(
            "Введите электронную почту/логин",
        ),
    )
    password = django.forms.PasswordInput()

    class Meta:
        model = django.contrib.auth.models.User
        fields = ["username", "password"]
