__all__ = ()

import django.forms
import django.utils.timezone
import django.utils.translation

import vacancies.models
import tinymce.widgets


class VacancyForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        self.fields["deadline"].widget.format = "%Y-%m-%d"

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < django.utils.timezone.now().date():
            raise django.forms.ValidationError(
                django.utils.translation.gettext_lazy(
                    "Дедлайн не может быть в прошлом.",
                ),
            )

        return deadline

    def clean_experience(self):
        experience = self.cleaned_data.get("required_experience")
        if experience is not None and experience < 0:
            raise django.forms.ValidationError(
                django.utils.translation.gettext_lazy(
                    "Опыт работы не может быть отрицательным.",
                ),
            )

        return experience

    class Meta:
        model = vacancies.models.Vacancy
        fields = [
            "title",
            "description",
            "hackaton_title",
            "deadline",
            "required_experience",
        ]
        widgets = {
            "title": django.forms.TextInput(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите название вакансии",
                    ),
                },
            ),
            "description": tinymce.widgets.TinyMCE(
                attrs={
                    "cols": 80,
                    "rows": 20,
                },
            ),
            "hackaton_title": django.forms.TextInput(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите название хакатона",
                    ),
                },
            ),
            "deadline": django.forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Выберите дедлайн",
                    ),
                },
            ),
            "required_experience": django.forms.NumberInput(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите требуемый опыт (в годах)",
                    ),
                },
            ),
        }


class CommentForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = vacancies.models.CommentVacancy
        fields = [
            model.comment.field.name,
        ]

        labels = {
            model.comment.field.name: "",
        }

        widgets = {
            model.comment.field.name: django.forms.Textarea(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите ваш комментарий",
                    ),
                    "rows": 3,
                },
            ),
        }
