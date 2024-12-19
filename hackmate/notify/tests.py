__all__ = ()

import django.contrib.auth
import django.test
import django.urls
import notifications.models

import vacancies.models


user_model = django.contrib.auth.get_user_model()


class NotificationsTests(django.test.TestCase):
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

        cls.vacancy2 = vacancies.models.Vacancy.objects.create(
            title="Test vacancy2",
            description="Test vacancy description2",
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

    def test_create_notifications(self):
        self.client.force_login(self.user)
        count_notifications = (
            notifications.models.Notification.objects.all().count()
        )
        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                kwargs={"pk": self.vacancy.pk},
            ),
        )
        count_notifications_after_request = (
            notifications.models.Notification.objects.all().count()
        )
        self.assertEqual(
            count_notifications_after_request,
            count_notifications + 1,
        )

    def test_read_all_notifications(self):
        self.client.force_login(self.user2)
        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                kwargs={"pk": self.vacancy.pk},
            ),
        )

        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                kwargs={"pk": self.vacancy2.pk},
            ),
        )
        self.client.get(
            django.urls.reverse(
                "notify:readall_notifications",
            ),
        )
        count_notifications_after_request = (
            notifications.models.Notification.objects.filter(
                unread=False,
                recipient=self.user,
            ).count()
        )
        self.assertEqual(
            count_notifications_after_request,
            0,
        )

    def test_read_one_notifications(self):
        client2 = django.test.Client()
        client2.force_login(self.user2)
        client2.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.pk],
            ),
        )
        client2.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy2.pk],
            ),
        )
        count_notifications = notifications.models.Notification.objects.filter(
            unread=True,
        ).count()
        client1 = django.test.Client()
        client1.force_login(self.user)
        client1.get(
            django.urls.reverse(
                "notify:readone_notification",
                args=[self.vacancy2.pk],
            ),
        )

        count_notifications_after_request = (
            notifications.models.Notification.objects.filter(
                unread=True,
            ).count()
        )

        self.assertEqual(
            count_notifications_after_request,
            count_notifications - 1,
        )

    def test_other_delete_your_notification(self):
        self.client.force_login(self.user2)
        self.client.post(
            django.urls.reverse(
                "vacancies:vacancy_detail",
                args=[self.vacancy.pk],
            ),
        )
        count_notifications = notifications.models.Notification.objects.filter(
            unread=True,
        ).count()

        self.client.get(
            django.urls.reverse(
                "notify:readone_notification",
                args=[self.vacancy.pk],
            ),
        )

        count_notifications_after_request = (
            notifications.models.Notification.objects.filter(
                unread=True,
            ).count()
        )

        self.assertEqual(
            count_notifications,
            count_notifications_after_request,
        )
