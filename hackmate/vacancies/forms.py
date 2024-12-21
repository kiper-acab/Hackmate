__all__ = ()

import re

import django.forms
import django.utils.timezone
import django.utils.translation
import tinymce.widgets

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
        current_date = django.utils.timezone.localdate(
            django.utils.timezone.now(),
        )

        if hackaton_date and hackaton_date < current_date:
            raise django.forms.ValidationError(
                django.utils.translation.gettext_lazy(
                    "Хакатон может быть в прошлом.",
                ),
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
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите название вакансии",
                    ),
                },
            ),
            model.description.field.name: tinymce.widgets.TinyMCE(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите описание",
                    ),
                },
            ),
            model.hackaton_title.field.name: django.forms.TextInput(
                attrs={
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Введите название хакатона",
                    ),
                },
            ),
            model.hackaton_date.field.name: django.forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": django.utils.translation.gettext_lazy(
                        "Выберите дату проведения хакатона",
                    ),
                },
            ),
        }


class CommentForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    def clean_comment(self):
        description = self.cleaned_data.get("comment")
        pattern = (
            r"(?iu)(?<![а-яё])"
            r"(?:(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|"
            r"(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|"
            r"(?:\S(?=[а-яё]))+?[оаеи-])-?)?"
            r"(?:[её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|"
            r"и[пб][ае][тцд][ьъ]).*?|"
            r"(?:(?:н[иеа]|(?:ра|и)[зс]|[зд]?[ао](?:т|дн[оа])?|"
            r"с(?:м[еи])?|а[пб]ч|в[ъы]?|пр[еи])-?)?"
            r"ху(?:[яйиеёю]|л+и(?!ган)).*?|"
            r"бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|"
            r"\S*?(?:п(?:[иеё]зд|ид[аое]?р|ед(?:р(?!о[рй]|рач)|"
            r"[аое]р|ик)|охую)|бля(?:[дбц]|тс)|"
            r"[ое]ху[яйиеё]|хуйн).*?|"
            r"(?:о[тб]?|про|на|вы)?м(?:анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|"
            r"ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]ь|ища)|"
            r"уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|"
            r"[ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й))|"
            r"елд[ауые].*?|ля[тд]ь|(?:[нз]а|по)х)"
            r"(?![а-яё])"
        )
        if re.search(pattern, description):
            return (
                "Комментарий не будет показан так как в нём "
                "присутствует ненормативная лексика"
            )

        return description

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
