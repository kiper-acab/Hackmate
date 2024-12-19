__all__ = ()

import django.forms
import django.utils.timezone

import vacancies.models


class VacancyForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        self.fields["hackaton_date"].widget.format = "%Y-%m-%d"
        self.fields["need_count_users"].required = True

    def clean_hackaton_date(self):
        hackaton_date = self.cleaned_data.get("hackaton_date")
        if (
            hackaton_date
            and hackaton_date < django.utils.timezone.now().date()
        ):
            raise django.forms.ValidationError(
                "Дедлайн не может быть в прошлом.",
            )

        return hackaton_date

    class Meta:
        model = vacancies.models.Vacancy
        fields = [
            model.title.field.name,
            model.description.field.name,
            model.need_count_users.field.name,
            model.hackaton_title.field.name,
            model.hackaton_date.field.name,
            model.required_experience.field.name,
        ]
        widgets = {
            model.title.field.name: django.forms.TextInput(
                attrs={"placeholder": "Введите название вакансии"},
            ),
            model.description.field.name: django.forms.Textarea(
                attrs={"placeholder": "Введите описание"},
            ),
            model.hackaton_title.field.name: django.forms.TextInput(
                attrs={"placeholder": "Введите название хакатона"},
            ),
            model.hackaton_date.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "Выберите дедлайн",
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
                    "placeholder": "Введите ваш комментарий",
                    "rows": 3,
                },
            ),
        }
