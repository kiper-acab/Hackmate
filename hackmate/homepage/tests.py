__all__ = ()

import http

import django.test
import django.urls
import parametrize


class OkResponseTests(django.test.TestCase):
    @parametrize.parametrize(
        "url",
        [
            (django.urls.reverse("homepage:homepage")),
        ],
    )
    def test_ok_response_test(self, url):
        response = self.client.get(url)
        self.assertEqual(http.HTTPStatus.OK, response.status_code)
