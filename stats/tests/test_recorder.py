from django.test import SimpleTestCase
from django.conf import settings
import time
from stats.recorder import StatsRecorder


class TestStatsRecorder(SimpleTestCase):

    def setUp(self):
        self.attack_data = dict(
            attacker_ip='127.0.0.1',
            service_name='Company Wordpress System',
            protocol='http',
            port='80',

            longitude="111.333333",
            latitude="222.33333",
            country='TH',
            country_name='Thailand',
            geo_location='Bangkok, Thailand'
        )
        self.recorder = StatsRecorder(self.attack_data)

    def tearDown(self):
        time.sleep(settings.TESTING_SLEEP_TIME)
        self.recorder.delete_table()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_save_banned_ip_success(self):

        banned_ip_record = self.recorder.save_banned_ip_record()
        self.assertEqual(banned_ip_record.category, 'blocked_ip_127.0.0.1')
        self.assertEqual(banned_ip_record.key, '127.0.0.1')
        self.assertEqual(banned_ip_record.protocol, 'http')
        self.assertEqual(banned_ip_record.port, '80')
        self.assertEqual(banned_ip_record.service_name, 'Company Wordpress System')
        self.assertEqual(banned_ip_record.longitude, "111.333333")
        self.assertEqual(banned_ip_record.latitude, "222.33333")
        self.assertEqual(banned_ip_record.geo_location, 'Bangkok, Thailand')

        self.assertEqual(banned_ip_record.count, 1)
        self.assertTrue(banned_ip_record.last_seen)

        banned_ip_record_2 = self.recorder.save_banned_ip_record()
        self.assertEqual(banned_ip_record_2.count, 2)

    def test_save_attacked_protocol_success(self):

        attacked_protocol_record = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record.category, 'attacked_service')
        self.assertEqual(attacked_protocol_record.key, 'Company Wordpress System')
        self.assertEqual(attacked_protocol_record.count, 1)

        attacked_protocol_record_2 = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record_2.category, 'attacked_service')
        self.assertEqual(attacked_protocol_record_2.key, 'Company Wordpress System')
        self.assertEqual(attacked_protocol_record_2.count, 2)

    def test_save_blocked_country_success(self):
        blocked_country_record = self.recorder.save_blocked_country_record()
        self.assertEqual(blocked_country_record.category, 'blocked_country')
        self.assertEqual(blocked_country_record.key, 'TH')
        self.assertEqual(blocked_country_record.country_name, 'Thailand')
        self.assertEqual(blocked_country_record.count, 1)