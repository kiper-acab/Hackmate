__all__ = ()

import django.forms

import vacancies.models


class VacancyForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = vacancies.models.Vacancy
        fields = [
            model.title.field.name,
            model.description.field.name,
        ]
        widgets = {
            model.title.field.name: django.forms.TextInput(
                attrs={
                    "placeholder": "Введите название вакансии",
                },
            ),
            model.description.field.name: django.forms.Textarea(
                attrs={
                    "placeholder": "Введите описание",
                },
            ),
        }
