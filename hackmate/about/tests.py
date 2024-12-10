__all__ = ()

import http

import django.test
import django.urls
import parametrize


class OkResponseTests(django.test.TestCase):
    @parametrize.parametrize(
        "url",
        [
            (django.urls.reverse("about:about")),
            (django.urls.reverse("about:contact")),
            (django.urls.reverse("about:privacy")),
        ],
    )
    def test_ok_response(self, url):
        response = self.client.get(url)
        self.assertEqual(http.HTTPStatus.OK, response.status_code)
