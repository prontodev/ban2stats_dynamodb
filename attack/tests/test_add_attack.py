from django.test import SimpleTestCase
from django.conf import settings
from attack.models import Attack
from stats.models import BlockedIP, AttackedService, BlockedCountry
from ban2stats.utils.tables import create_all, delete_all
import time
import json
from pynamodb.exceptions import TableDoesNotExist


class TestAttackAdd(SimpleTestCase):

    def tearDown(self):
        delete_all()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def setUp(self):
        create_all()
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

        blocked_ip_from_db = BlockedIP.scan() #query("37.419200897216797,-122.05740356445312")
        counter = 0
        for item in blocked_ip_from_db:
            counter += 1
            lat, lon = item.lat_lon.split(',')
            self.assertAlmostEqual(float(lat), 37.419200897216797)
            self.assertAlmostEqual(float(lon), -122.05740356445312)
            attack_details = json.loads(item.attack_details)
            self.assertEqual(attack_details["72.14.207.99"]["count"], 1)

        self.assertEqual(counter, 1)

        attacked_protocol_from_db = AttackedService.query('company web server test view')
        counter = 0
        for item in attacked_protocol_from_db:
            counter += 1
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

        blocked_country_from_db = BlockedCountry.query('US')
        counter = 0
        for item in blocked_country_from_db:
            counter += 1
            self.assertEqual(item.country_code, 'US')
            self.assertEqual(item.country_name, 'United States')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

        self.assertContains(response, 'Added attack')

    def test_add_two_distinct_location(self):
        self.reset_stats()
        fail2ban_data = dict(
            attacker_ip='72.14.207.99',
            service_name='company web server test view',
            protocol='http',
            port='81',
        )
        response = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)

        fail2ban_data = dict(
            attacker_ip='114.109.35.4',
            service_name='HR Portal',
            protocol='http',
            port='9090',
        )
        response2 = self.client.post('/attack/new/', data=fail2ban_data, **self.request_headers)
        time.sleep(2)

        attacks_from_db = Attack.query('72.14.207.99', port='81')
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.port, '81')
            counter += 1
        self.assertEqual(counter, 1)

        blocked_ip_from_db = BlockedIP.scan()#query("37.419200897216797,-122.05740356445312")
        counter = 0
        ip_starts_with_72 = None
        ip_starts_with_114 = None
        for item in blocked_ip_from_db:
            if item.lat_lon.startswith('37'):
                ip_starts_with_72 = item
            else:
                ip_starts_with_114 = item
            counter += 1
        self.assertEqual(counter, 2)
        lat, lon = ip_starts_with_72.lat_lon.split(',')
        self.assertAlmostEqual(float(lat), 37.419200897216797)
        self.assertAlmostEqual(float(lon), -122.05740356445312)
        attack_details = json.loads(ip_starts_with_72.attack_details)
        self.assertEqual(attack_details["72.14.207.99"]["count"], 1)


        attacked_protocol_from_db = AttackedService.query('company web server test view')
        counter = 0
        for item in attacked_protocol_from_db:
            counter += 1
            self.assertEqual(item.service_name, 'company web server test view')
            self.assertEqual(item.count, 1)
        self.assertEqual(counter, 1)

        blocked_country_from_db = BlockedCountry.query('US')
        counter = 0
        for item in blocked_country_from_db:
            counter += 1
            self.assertEqual(item.country_code, 'US')
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