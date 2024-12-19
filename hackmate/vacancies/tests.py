__all__ = ()

import json

import django.contrib.auth
import django.contrib.messages
import django.test
import django.urls
import django.utils
import parametrize

import vacancies.models


user_model = django.contrib.auth.get_user_model()


class VacanciesTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = user_model.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testuser123",
        )

        cls.user2 = user_model.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="testuser123",
        )

        cls.superuser = user_model.objects.create_user(
            username="superadmin",
            email="superadmin@example.com",
            password="superadmin123",
            is_superuser=True,
        )

        cls.vacancy = vacancies.models.Vacancy.objects.create(
            title="Test vacancy",
            description="Test vacancy description",
            creater=cls.user,
            status=vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
            need_count_users=2,
        )

        cls.comment = vacancies.models.CommentVacancy.objects.create(
            vacancy=cls.vacancy,
            user=cls.user,
            comment="Test comment",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.user2.delete()
        cls.vacancy.delete()
        cls.comment.delete()
        cls.superuser.delete()

    def test_correct_create_vacancy(self):
        self.client.force_login(self.user)
        data = {
            vacancies.models.Vacancy.title.field.name: "title",
            vacancies.models.Vacancy.description.field.name: "description",
            vacancies.models.Vacancy.need_count_users.field.name: 2,
            vacancies.models.Vacancy.required_experience.field.name: (
                vacancies.models.Vacancy.RequiredExperienceСhoices.BIGGINER,
            ),
        }
        vacancy_count = vacancies.models.Vacancy.objects.all().count()

        self.client.post(
            django.urls.reverse("vacancies:vacancy_create"),
            data=data,
        )
        vacancy_count_after_create = (
            vacancies.models.Vacancy.objects.all().count()
        )
        self.assertEqual(vacancy_count, vacancy_count_after_create - 1)

    def test_create_vacancy_not_authenticate_user(self):
        model = vacancies.models.Vacancy
        data = {
            model.title.field.name: "title",
            model.description.field.name: "description",
            model.hackaton_title.field.name: "hackaton_title",
        }
        vacancy_count = vacancies.models.Vacancy.objects.all().count()
        self.client.post(
            django.urls.reverse("vacancies:vacancy_create"),
            data=data,
        )
        vacancy_count_after_create = (
            vacancies.models.Vacancy.objects.all().count()
        )
        self.assertEqual(vacancy_count, vacancy_count_after_create)

    @parametrize.parametrize(
        "data",
        [
            (
                {
                    (
                        vacancies.models.Vacancy.description.field.name
                    ): "description",
                },
            ),
            ({vacancies.models.Vacancy.title.field.name: "title"},),
        ],
    )
    def test_create_inccorect_vacancy(self, data):
        self.client.force_login(self.user)
        vacancy_count = vacancies.models.Vacancy.objects.all().count()
        self.client.post(
            django.urls.reverse("vacancies:vacancy_create"),
            data=data,
        )
        vacancy_count_after_create = (
            vacancies.models.Vacancy.objects.all().count()
        )

        self.assertEqual(vacancy_count, vacancy_count_after_create)

    def test_response_vacancy_create_authenticate_user(self):
        self.client.force_login(self.user)
        count_responses = vacancies.models.Response.objects.all().count()
        response = self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertIn("Ваш отклик отправлен!", response_json["message"])

        count_responses_after_request = (
            vacancies.models.Response.objects.all().count()
        )
        self.assertEqual(count_responses, count_responses_after_request - 1)

    def test_response_vacancy_create_not_authenticate_user(self):
        count_responses = vacancies.models.Response.objects.all().count()
        response = self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )
        response_json = json.loads(response.content.decode("utf-8"))
        self.assertIn("Вы должны быть авторизованы", response_json["error"])

        count_responses_after_request = (
            vacancies.models.Response.objects.all().count()
        )
        self.assertEqual(count_responses, count_responses_after_request)

    def test_update_vacancy_views(self):
        model = vacancies.models.Vacancy
        views_count = model.objects.get(pk=self.vacancy.pk).views.all().count()

        self.client.get(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )

        views_count_after_request = (
            model.objects.get(pk=self.vacancy.pk).views.all().count()
        )
        self.assertEqual(views_count, views_count_after_request - 1)

    def test_dont_update_vacancy_views_after_the_same_ip(self):
        model = vacancies.models.Vacancy
        views_count = model.objects.get(pk=self.vacancy.pk).views.all().count()

        for _ in range(2):
            self.client.get(
                django.urls.reverse(
                    "vacancies:vacancy_detail",
                    args=[self.vacancy.id],
                ),
            )

        views_count_after_request = (
            model.objects.get(pk=self.vacancy.pk).views.all().count()
        )
        self.assertEqual(views_count, views_count_after_request - 1)

    def test_add_comments(self):
        data = {
            (
                vacancies.models.CommentVacancy.comment.field.name
            ): "Test comment",
        }
        self.client.force_login(self.user)
        count_comments = vacancies.models.CommentVacancy.objects.all().count()
        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
            data=data,
        )
        count_comments_after_request = (
            vacancies.models.CommentVacancy.objects.all().count()
        )
        self.assertEqual(count_comments, count_comments_after_request - 1)

    def test_delete_comments(self):
        self.client.force_login(self.user)
        count_comments = vacancies.models.CommentVacancy.objects.all().count()
        self.client.get(
            django.urls.reverse(
                "vacancies:delete_comment",
                args=[self.comment.id],
            ),
        )
        count_comments_after_request = (
            vacancies.models.CommentVacancy.objects.all().count()
        )
        self.assertEqual(count_comments, count_comments_after_request + 1)

    def test_other_people_delete_your_comment(self):
        self.client.force_login(self.user2)
        count_comments = vacancies.models.CommentVacancy.objects.all().count()
        self.client.get(
            django.urls.reverse(
                "vacancies:delete_comment",
                args=[self.comment.id],
            ),
        )
        count_comments_after_request = (
            vacancies.models.CommentVacancy.objects.all().count()
        )
        self.assertEqual(count_comments, count_comments_after_request)

    def test_superadmin_delete_your_comment(self):
        self.client.force_login(self.superuser)
        count_comments = vacancies.models.CommentVacancy.objects.all().count()
        self.client.get(
            django.urls.reverse(
                "vacancies:delete_comment",
                args=[self.comment.id],
            ),
        )
        count_comments_after_request = (
            vacancies.models.CommentVacancy.objects.all().count()
        )
        self.assertEqual(count_comments, count_comments_after_request + 1)

    def test_create_response(self):
        self.client.force_login(self.user2)
        count_responses = vacancies.models.Response.objects.filter(
            user=self.user2,
        ).count()
        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )
        count_responses_after_request = (
            vacancies.models.Response.objects.filter(user=self.user2).count()
        )
        self.assertEqual(count_responses, count_responses_after_request - 1)

    def test_create_the_same_request(self):
        self.client.force_login(self.user2)
        count_responses = vacancies.models.Response.objects.filter(
            user=self.user2,
        ).count()

        for _ in range(2):
            response = self.client.post(
                django.urls.reverse(
                    "vacancies:vacancy_detail",
                    args=[self.vacancy.id],
                ),
            )

        count_responses_after_request = len(
            vacancies.models.Response.objects.filter(user=self.user2),
        )
        self.assertEqual(count_responses, count_responses_after_request - 1)

        response_json = json.loads(response.content.decode("utf-8"))
        self.assertIn(
            "Вы уже откликнулись на эту вакансию",
            response_json["message"],
        )


class InviteUserTestCase(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = user_model.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testuser123",
        )

        cls.user2 = user_model.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="testuser123",
        )

        cls.vacancy = vacancies.models.Vacancy.objects.create(
            title="Test vacancy",
            description="Test vacancy description",
            creater=cls.user,
            status=vacancies.models.Vacancy.VacancyStatuses.ACTIVE,
            need_count_users=2,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.user2.delete()
        cls.vacancy.delete()

    def test_invite_user(self):
        self.client.force_login(self.user2)

        count_temmates = self.vacancy.team_composition.count()

        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )

        response = vacancies.models.Response.objects.get(
            vacancy=self.vacancy,
            user=self.user2,
        )

        self.client.force_login(self.user)
        self.client.get(
            django.urls.reverse(
                "vacancies:invite_user",
                args=[response.id],
            ),
        )

        response.refresh_from_db()

        self.assertEqual(
            response.status,
            vacancies.models.Response.ResponseStatuses.ACCEPTED,
        )

        self.assertEqual(
            self.vacancy.team_composition.count(),
            count_temmates + 1,
        )

    def test_reject_invite(self):
        self.client.force_login(self.user2)

        count_temmates = self.vacancy.team_composition.count()

        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.id],
            ),
        )

        response = vacancies.models.Response.objects.get(
            vacancy=self.vacancy,
            user=self.user2,
        )

        self.client.force_login(self.user)
        self.client.get(
            django.urls.reverse(
                "vacancies:reject_user",
                args=[response.id],
            ),
        )

        response.refresh_from_db()

        self.assertEqual(
            response.status,
            vacancies.models.Response.ResponseStatuses.REJECTED,
        )

        self.assertEqual(
            self.vacancy.team_composition.count(),
            count_temmates,
        )
