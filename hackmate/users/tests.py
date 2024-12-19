__all__ = ()

import datetime
import http

import django.contrib.auth.models
import django.contrib.messages
import django.test
import django.urls
import django.utils
import django.utils.timezone
import parametrize

import users.forms
import users.models

user_model = django.contrib.auth.models.User


class SignupTest(django.test.TestCase):
    def test_corrcet_create_new_user(self):
        data = {
            "username": "TestUserName",
            "email": "testemail@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        users.forms.UserCreateForm(data).save()
        count_models = user_model.objects.all().count()
        self.assertEqual(count_models, 1)

    def test_create_user_not_equal_passwords(self):
        data = {
            "username": "TestUserName",
            "email": "testemail@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword1234567890",
        }
        response = self.client.post(django.urls.reverse("users:signup"), data)
        count_models = user_model.objects.all().count()
        self.assertTrue(response.context["form"].has_error("password2"))
        self.assertEqual(count_models, 0)

    def test_create_user_name_exists(self):
        data1 = {
            "username": "TestUserName",
            "email": "testemail@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

        data2 = {
            "username": "TestUserName",
            "email": "testemail2@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

        self.client.post(django.urls.reverse("users:signup"), data1)
        response = self.client.post(django.urls.reverse("users:signup"), data2)
        count_models = user_model.objects.all().count()

        self.assertTrue(response.context["form"].has_error("username"))
        self.assertEqual(count_models, 1)

    def test_create_users_profile(self):
        data = {
            "username": "TestUserName2",
            "email": "testemail@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        self.client.post(django.urls.reverse("users:signup"), data)
        count_models = users.models.Profile.objects.all().count()
        self.assertEqual(count_models, 1)


class ActivateUserTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user_model = django.contrib.auth.models.User

        cls.not_active_data = {
            "username": "TestNotActiveUserName",
            "email": "testemail1@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "is_active": False,
        }

        cls.user_not_active = user_model.objects.create_user(
            username=cls.not_active_data["username"],
            email=cls.not_active_data["email"],
            password=cls.not_active_data["password1"],
            is_active=cls.not_active_data["is_active"],
        )

        cls.data_active = {
            "username": "TestActiveUserName",
            "email": "testemail2@mail.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "is_active": True,
        }

        cls.user_active = user_model.objects.create_user(
            username=cls.data_active["username"],
            email=cls.data_active["email"],
            password=cls.data_active["password1"],
            is_active=cls.data_active["is_active"],
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.user_not_active.delete()
        cls.user_active.delete()

    def test_not_activate_user(self):
        response = self.client.get(
            django.urls.reverse(
                "users:activate",
                args=["TestNotActiveUserName"],
            ),
        )
        messages = list(
            django.contrib.messages.get_messages(response.wsgi_request),
        )

        self.assertTrue(
            any(
                "Пользователь успешно активирован" in str(m) for m in messages
            ),
        )

    def test_active_user(self):
        response = self.client.get(
            django.urls.reverse(
                "users:activate",
                args=["TestActiveUserName"],
            ),
        )
        messages = list(
            django.contrib.messages.get_messages(response.wsgi_request),
        )

        self.assertTrue(
            any("Пользователь уже активирован" in str(m) for m in messages),
        )

    def test_not_real_user(self):
        response = self.client.get(
            django.urls.reverse("users:activate", args=["NotRealUSer"]),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)


class TestAuthinicateUser(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        model = django.contrib.auth.models.User
        cls.user = model.objects.create_user(
            username="TestUser",
            email="testemail@mail.com",
            password="Testpassword123",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    @parametrize.parametrize(
        "username,password",
        [
            ("TestUser", "Testpassword123"),
            ("testemail@mail.com", "Testpassword123"),
        ],
    )
    def test_login_user(self, username, password):
        data = {
            "username": username,
            "password": password,
        }
        response = self.client.post(django.urls.reverse("users:login"), data)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_wrong_password_login_user(self):
        data = {
            "username": "TestUser",
            "password": "WrongPassword123",
        }
        response = self.client.post(django.urls.reverse("users:login"), data)

        self.assertFalse(response.wsgi_request.user.is_authenticated)


class NormalEmailTests(django.test.TestCase):

    def test_has_user_mail_normal_form(self):
        data = {
            "email": "testmail@ya.ru",
            "username": "TestLogin123456",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        }
        self.client.post(django.urls.reverse("users:signup"), data)
        user = user_model.objects.get(username="TestLogin123456")
        self.assertEqual(user.email, "testmail@yandex.ru")

    @django.test.override_settings(MAX_AUTH_ATTEMPTS=5)
    def lock_user_after_some_failed_attempts(self):
        data = {
            "email": "test.mail@ya.ru",
            "username": "TestLogin123456",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
        }
        self.client.post(django.urls.reverse("users:signup"), data)
        user = user_model.objects.get(username="TestLogin123456")

        for _ in range(5):
            self.client.post(
                django.urls.reverse("users:login"),
                {"username": "TestLogin123456", "password": "wrongpassword"},
            )

        self.assertFa(user.is_active)

    def test_corrcet_activate_user_after_lock(self):
        data = {
            "email": "test.mail@ya.ru",
            "username": "TestLogin123456",
            "password": "Testpassword123",
        }

        user = users.models.User.objects.create_user(
            email=data["email"],
            password=data["password"],
            username=data["username"],
            is_active=False,
        )
        user = users.models.User.objects.get(username=user.username)
        profile = users.models.Profile.objects.get(
            user=user,
        )
        profile.date_last_active = (
            django.utils.timezone.now() - datetime.timedelta(days=1)
        )
        profile.save()

        response = self.client.get(
            django.urls.reverse("users:activate", args=[user.username]),
        )

        messages = list(
            django.contrib.messages.get_messages(response.wsgi_request),
        )

        self.assertTrue(
            any(
                "Пользователь успешно активирован" in str(m) for m in messages
            ),
        )

    def test_uncorrcet_activate_user_after_lock(self):
        data = {
            "email": "test.mail@ya.ru",
            "username": "TestLogin123456",
            "password": "Testpassword123",
        }

        user = users.models.User.objects.create_user(
            email=data["email"],
            password=data["password"],
            username=data["username"],
            is_active=False,
        )

        user.profile.date_last_active = (
            django.utils.timezone.now() - datetime.timedelta(days=14)
        )
        user.profile.save()

        response = self.client.get(
            django.urls.reverse("users:activate", args=[user.username]),
        )

        messages = list(
            django.contrib.messages.get_messages(response.wsgi_request),
        )

        self.assertTrue(
            any(
                "Активация профиля была доступна в течение" in str(m)
                for m in messages
            ),
        )


class DeleteLinkViewTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "testpassword",
        }
        cls.user = users.models.User.objects.create_user(
            email=cls.data["email"],
            password=cls.data["password"],
            username=cls.data["username"],
            is_active=True,
        )
        profile = users.models.Profile.objects.get(
            user=cls.user,
        )
        cls.link = users.models.ProfileLink.objects.create(
            profile=profile,
            site_type="GitLab",
            url="http://example.com",
        )

        cls.owner_data = {
            "email": "owner@test.com",
            "username": "owneruser",
            "password": "ownerpassword",
        }
        cls.owner = users.models.User.objects.create_user(
            email=cls.owner_data["email"],
            password=cls.owner_data["password"],
            username=cls.owner_data["username"],
            is_active=True,
        )
        cls.profile_owner = users.models.Profile.objects.get(user=cls.owner)
        cls.owner_link = users.models.ProfileLink.objects.create(
            profile=cls.profile_owner,
            site_type="GitLab",
            url="http://example.com",
        )

        cls.other_user_data = {
            "email": "other@test.com",
            "username": "otheruser",
            "password": "password123",
        }
        cls.other_user = users.models.User.objects.create_user(
            email=cls.other_user_data["email"],
            password=cls.other_user_data["password"],
            username=cls.other_user_data["username"],
            is_active=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.link.delete()
        cls.owner_link.delete()
        cls.user.delete()
        cls.owner.delete()
        cls.other_user.delete()
        super().tearDownClass()

    def test_delete_link(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            django.urls.reverse("users:delete_link", args=[self.link.pk]),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("users:profile_edit"),
        )
        self.assertFalse(
            users.models.ProfileLink.objects.filter(pk=self.link.pk).exists(),
        )

    def test_delete_link_other_user(self):
        self.client.login(
            username=self.other_user_data["username"],
            password=self.other_user_data["password"],
        )

        response = self.client.get(
            django.urls.reverse("users:delete_link", args=[self.link.pk]),
        )

        self.assertRedirects(
            response,
            django.urls.reverse("users:profile_edit"),
        )

        self.assertTrue(
            users.models.ProfileLink.objects.filter(pk=self.link.pk).exists(),
        )


class ProfileViewTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "testpassword",
        }
        cls.other_user_data = {
            "email": "other@test.com",
            "username": "otheruser",
            "password": "password123",
        }

        cls.user = users.models.User.objects.create_user(
            email=cls.user_data["email"],
            password=cls.user_data["password"],
            username=cls.user_data["username"],
        )
        cls.profile = users.models.Profile.objects.get(user=cls.user)

        cls.other_user = users.models.User.objects.create_user(
            email=cls.other_user_data["email"],
            password=cls.other_user_data["password"],
            username=cls.other_user_data["username"],
        )
        cls.other_profile = users.models.Profile.objects.get(
            user=cls.other_user,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.profile.delete()
        cls.other_user.delete()
        cls.other_profile.delete()
        super().tearDownClass()

    def test_profile_view_profile(self):
        url = django.urls.reverse(
            "users:profile",
            kwargs={"username": self.user.username},
        )
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertTrue(response.context["is_own_profile"])

    def test_profile_view_other_user(self):
        url = django.urls.reverse(
            "users:profile",
            kwargs={"username": self.other_user.username},
        )
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.other_user.username)
        self.assertFalse(response.context["is_own_profile"])


class ProfileEditViewTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = users.models.User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        cls.profile = users.models.Profile.objects.get(user=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.profile.delete()
        super().tearDownClass()

    def test_get_profile_edit_view(self):
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_edit.html")
        self.assertIn("form", response.context)
        self.assertIn("profile_form", response.context)
        self.assertIn("link_form", response.context)

    def test_update_profile(self):
        data = {
            "email": "newemail@test.com",
            "username": "newusername",
        }
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(url, data=data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@test.com")
        self.assertEqual(self.user.username, "newusername")
        self.assertRedirects(response, url)

    def test_correct_birthday(self):
        norm_date = datetime.date(2000, 9, 1)
        data = {
            "email": "newemail@test.com",
            "username": "newusername",
            "birthday": norm_date,
        }
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(url, data=data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.birthday, norm_date)
        self.assertRedirects(response, url)

    def test_uncorrected_birthday(self):
        future_date = datetime.date(2100, 9, 1)
        data = {
            "email": "newemail@test.com",
            "username": "newusername",
            "birthday": future_date,
        }
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        self.client.post(url, data=data)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.profile.birthday, future_date)

    def test_uncorrected_birthday_before(self):
        before_date = datetime.date(1500, 9, 1)
        data = {
            "email": "newemail@test.com",
            "username": "newusername",
            "birthday": before_date,
        }
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        self.client.post(url, data=data)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.profile.birthday, before_date)

    def test_missing_required_fields(self):
        data = {"email": "", "username": ""}
        url = django.urls.reverse("users:profile_edit")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Поля Email и Username обязательны для заполнения.",
        )
