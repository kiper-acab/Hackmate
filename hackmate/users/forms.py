__all__ = []

import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

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
            field.field.required = False

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
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        fields = (
            UserChangeForm.Meta.model.email.field.name,
            UserChangeForm.Meta.model.username.field.name,
            "password1",
            "password2",
        )

        labels = {
            UserChangeForm.Meta.model.username.field.name: "Введите логин",
        }


class ProfileChangeForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.required = False

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.image.field.name,
            users.models.Profile.birthday.field.name,
            users.models.Profile.description.field.name,
        )

        labels = {
            users.models.Profile.image.field.name: "Выберите себе картинку",
            users.models.Profile.description.field.name: "Описание",
        }

        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                },
                format=("%Y-%m-%d"),
            ),
        }


class AuthenticateForm(
    django.contrib.auth.forms.AuthenticationForm,
    BootstrapForm,
):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["password"].widget.label = "Пароль"

    username = django.forms.CharField(label="Введите электронную почту/логин")
    password = django.forms.PasswordInput()

    class Meta:
        model = django.contrib.auth.models.User
        fields = ["username", "password"]
