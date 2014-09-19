from django.test import SimpleTestCase


class TestAttackAdd(SimpleTestCase):

    def test_add(self):
        fail2ban_data = dict(
            attacker_ip='127.0.0.1',
            service_name='company web server',
            protocol='http',
            port='80',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data)
        self.assertContains(response, 'Added attack')
