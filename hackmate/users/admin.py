__all__ = []

import django.contrib
import django.contrib.admin
import django.contrib.auth
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models

user = django.contrib.auth.get_user_model()


class ProfileInline(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    readonly_fields = (
        users.models.Profile.birthday.field.name,
        users.models.Profile.image.field.name,
    )


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


django.contrib.admin.site.unregister(user)
django.contrib.admin.site.register(user, UserAdmin)
