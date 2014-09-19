from django.test import SimpleTestCase


class TestAttackAdd(SimpleTestCase):

    def test_urls(self):
        response = self.client.get('/attack/new/')
        self.assertContains(response, 'Add attack')