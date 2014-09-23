from django.test import SimpleTestCase
from attack.models import Attack
import time


class TestAttackAdd(SimpleTestCase):

    def tearDown(self):
        Attack.delete_table()
        time.sleep(1)

    def setUp(self):
        if Attack.exists():
            Attack.delete_table()
            time.sleep(1)
        Attack.create_table(wait=True)

    def test_add(self):
        fail2ban_data = dict(
            attacker_ip='72.14.207.99',
            service_name='company web server test view',
            protocol='http',
            port='81',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data)

        attacks_from_db = Attack.query('72.14.207.99', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '81')
            counter += 1
        self.assertEqual(1, counter)
        self.assertContains(response, 'Added attack')
