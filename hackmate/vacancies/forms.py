__all__ = ()

import django.forms

import vacancies.models


class VacancyForm(django.forms.ModelForm):
    class Meta:
        model = vacancies.models.Vacancy
        fields = [
            model.title.field.name,
            model.description.field.name,
        ]
        widgets = {
            model.title.field.name: django.forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название вакансии",
                },
            ),
            model.description.field.name: django.forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание",
                },
            ),
        }
        labels = {
            "title": "Название вакансии",
            "description": "Описание вакансии",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
