__all__ = ()

import django.db
import django.db.models.deletion
import users.models
import users.validators


class Migration(django.db.migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        django.db.migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    django.db.models.CharField(
                        max_length=30,
                        verbose_name="страна",
                    ),
                ),
            ],
        ),
        django.db.migrations.AlterField(
            model_name="profile",
            name="birthday",
            field=django.db.models.DateField(
                blank=True,
                help_text="Введите дату рождения",
                null=True,
                validators=[users.validators.validate_birthday],
                verbose_name="день рождения",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="profile",
            name="description",
            field=django.db.models.TextField(
                blank=True,
                help_text="Расскажите о себе",
                null=True,
                verbose_name="о себе",
            ),
        ),
        django.db.migrations.AlterField(
            model_name="profile",
            name="image",
            field=django.db.models.ImageField(
                blank=True,
                null=True,
                upload_to=users.models.user_directory_path,
            ),
        ),
        django.db.migrations.CreateModel(
            name="ProfileLink",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "site_type",
                    django.db.models.CharField(
                        choices=[
                            ("facebook", "Facebook"),
                            ("twitter", "Twitter"),
                            ("instagram", "Instagram"),
                            ("vk", "VK"),
                            ("gitlub", "GitLub"),
                            ("github", "GitHub"),
                        ],
                        max_length=20,
                        verbose_name="тип сайта",
                    ),
                ),
                (
                    "url",
                    django.db.models.URLField(
                        blank=True,
                        help_text="Полная ссылка, "
                        "например, https://example.com",
                        null=True,
                        verbose_name="URL",
                    ),
                ),
                (
                    "profile",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        to="users.profile",
                        verbose_name="профиль",
                    ),
                ),
            ],
            options={
                "verbose_name": "ссылка",
                "verbose_name_plural": "ссылки",
            },
        ),
        django.db.migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    django.db.models.CharField(
                        max_length=30,
                        verbose_name="город",
                    ),
                ),
                (
                    "country",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.country",
                    ),
                ),
            ],
        ),
        django.db.migrations.AddField(
            model_name="profile",
            name="city",
            field=django.db.models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.city",
            ),
        ),
        django.db.migrations.AddField(
            model_name="profile",
            name="country",
            field=django.db.models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.country",
            ),
        ),
    ]
