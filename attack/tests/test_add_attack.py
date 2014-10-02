from django.test import SimpleTestCase
from attack.models import Attack
import time
from pynamodb.exceptions import TableDoesNotExist


class TestAttackAdd(SimpleTestCase):

    def tearDown(self):
        Attack.delete_table()
        time.sleep(1)

    def setUp(self):
        if Attack.exists():
            Attack.delete_table()
            time.sleep(1)
        try:
            Attack.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'
            Attack.create_table(wait=True)

        self.request_headers = {'HTTP_TOKEN': 'oTbCmV71i2Lg5wQMSsPEFKGJ0Banana'}

    def test_add(self):
        fail2ban_data = dict(
            attacker_ip='72.14.207.99',
            service_name='company web server test view',
            protocol='http',
            port='81',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)

        attacks_from_db = Attack.query('72.14.207.99', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '81')
            counter += 1
        self.assertEqual(1, counter)
        self.assertContains(response, 'Added attack')

    def test_add_fail__missing_parameter(self):
        fail2ban_data = dict()
        response = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)

        attacks_from_db = Attack.query('72.14.207.99', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '81')
            counter += 1
        self.assertEqual(0, counter)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Required attacker_ip, service_name, protocol and port.')

    def test_add_fail__invalid_IP(self):
        fail2ban_data = dict(
            attacker_ip='127.8.8.8',
            service_name='company web server test view: invalid ip',
            protocol='http',
            port='82',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)

        attacks_from_db = Attack.query('127.8.8.8', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '82')
            counter += 1
        self.assertEqual(0, counter)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Cannot find Geo details for this IP 127.8.8.8')