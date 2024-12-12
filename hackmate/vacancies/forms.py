__all__ = ()

import django.forms

import vacancies.models


class VacancyForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < django.utils.timezone.now().date():
            raise django.forms.ValidationError(
                "Дедлайн не может быть в прошлом.",
            )

        return deadline

    def clean_experience(self):
        experience = self.cleaned_data.get("required_experience")
        if experience is not None and experience < 0:
            raise django.forms.ValidationError(
                "Опыт работы не может быть отрицательным.",
            )

        return experience

    class Meta:
        model = vacancies.models.Vacancy
        fields = [
            model.title.field.name,
            model.description.field.name,
            model.hackaton_title.field.name,
            model.deadline.field.name,
            model.required_experience.field.name,
            model.role.field.name,
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
            model.deadline.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "Выберите дедлайн",
                },
            ),
            model.required_experience.field.name: django.forms.NumberInput(
                attrs={"placeholder": "Введите требуемый опыт (в годах)"},
            ),
            model.role.field.name: django.forms.Select(
                attrs={"placeholder": "Введите роль человека"},
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
