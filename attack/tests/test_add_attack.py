from django.test import SimpleTestCase
from attack.models import Attack
from stats.models import BlockedIP, AttackedService, BlockedCountry
import time
from pynamodb.exceptions import TableDoesNotExist, TableError


class TestAttackAdd(SimpleTestCase):

    def tearDown(self):
        Attack.delete_table()
        try:
            BlockedIP.delete_table()
        except TableDoesNotExist:
            pass
        except TableError:
            pass
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

    def reset_stats(self):
        blocked_ip_from_db = BlockedIP.query('72.14.207.99', category='blocked_ip_72.14.207.99')
        try:
            for item in blocked_ip_from_db:
                self.assertEqual(item.category, 'blocked_ip_72.14.207.99')
                self.assertEqual(item.key, '72.14.207.99')
                item.count = 0
                item.save()
        except TableDoesNotExist:
            pass

        attacked_protocol_from_db = AttackedService.query('http', category='attacked_service')
        try:
            for item in attacked_protocol_from_db:
                self.assertEqual(item.category, 'attacked_service')
                self.assertEqual(item.key, 'company web server test view')
                item.count = 0
                item.save()
        except TableDoesNotExist:
            pass

        blocked_country_from_db = BlockedCountry.query('US', category='blocked_country')
        try:
            for item in blocked_country_from_db:
                self.assertEqual(item.category, 'blocked_country')
                self.assertEqual(item.key, 'US')
                item.count = 0
                item.save()
        except TableDoesNotExist:
            pass

    def test_add(self):
        self.reset_stats()
        fail2ban_data = dict(
            attacker_ip='72.14.207.99',
            service_name='company web server test view',
            protocol='http',
            port='81',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)
        time.sleep(2)

        attacks_from_db = Attack.query('72.14.207.99', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '81')
            counter += 1
        self.assertEqual(counter, 1)

        blocked_ip_from_db = BlockedIP.query('blocked_ip_72.14.207.99', key='72.14.207.99')
        counter = 0
        for item in blocked_ip_from_db:
            counter += 1
            self.assertEqual(item.category, 'blocked_ip_72.14.207.99')
            self.assertEqual(item.key, u'72.14.207.99')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

        attacked_protocol_from_db = AttackedService.query('attacked_service', key='company web server test view')
        counter = 0
        for item in attacked_protocol_from_db:
            counter += 1
            self.assertEqual(item.category, 'attacked_service')
            self.assertEqual(item.key, 'company web server test view')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

        blocked_country_from_db = BlockedCountry.query('blocked_country', key='US')
        counter = 0
        for item in blocked_country_from_db:
            counter += 1
            self.assertEqual(item.category, 'blocked_country')
            self.assertEqual(item.key, 'US')
            self.assertEqual(item.country_name, 'United States')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

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