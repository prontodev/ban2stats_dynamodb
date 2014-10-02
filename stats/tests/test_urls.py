from django.test import SimpleTestCase


class URLTest(SimpleTestCase):

    def test_urls(self):
        response = self.client.get('/stats/')
        self.assertEqual(200, response.status_code)