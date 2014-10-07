from django.test import SimpleTestCase


class TestGetStatsViews(SimpleTestCase):

    def test_view(self):
        response = self.client.get('/stats/')
        self.assertContains(response, 'var blocked_ip_count = ')
        self.assertContains(response, 'var blocked_countries = [')
        self.assertContains(response, 'var blocked_ips = [')
        self.assertContains(response, 'var attacked_services = [')