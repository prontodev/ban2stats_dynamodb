from django.test import SimpleTestCase
from django.conf import settings
import time
import json
from stats.recorder import StatsRecorder
from stats.models import BlockedIP, AttackedService, BlockedCountry


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

        self.attack_data2 = dict(
            attacker_ip='127.0.0.2',
            service_name='Back office service',
            protocol='http',
            port='80',

            longitude="111.333333",
            latitude="222.33333",
            country='RU',
            country_name='Russia',
            geo_location='n/a, Russia'
        )
        self.recorder2 = StatsRecorder(self.attack_data2)

    def tearDown(self):
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_save_banned_ip_success(self):
        if not BlockedIP.exists():
            BlockedIP.create_table(wait=True)

        banned_ip_record = self.recorder.save_blocked_ip_record()
        self.assertEqual(banned_ip_record.lat_lon, '222.33333,111.333333')
        self.assertEqual(banned_ip_record.geo_location, 'Bangkok, Thailand')

        # print banned_ip_record.attack_details
        attack_details = json.loads(banned_ip_record.attack_details)
        self.assertEqual(attack_details['127.0.0.1']['protocol'], 'http')
        self.assertEqual(attack_details['127.0.0.1']['port'], '80')
        self.assertEqual(attack_details['127.0.0.1']['service_name'], 'Company Wordpress System')

        self.assertEqual(attack_details['127.0.0.1']['count'], 1)
        self.assertTrue(attack_details['127.0.0.1']['last_seen'])

        banned_ip_record_2 = self.recorder.save_blocked_ip_record()
        attack_details2 = json.loads(banned_ip_record_2.attack_details)
        self.assertEqual(attack_details2['127.0.0.1']['count'], 2)

        banned_ip_record_3 = self.recorder2.save_blocked_ip_record()
        attack_details3 = json.loads(banned_ip_record_3.attack_details)
        self.assertEqual(attack_details3['127.0.0.2']['count'], 1)

        banned_ip_record_4 = self.recorder.save_blocked_ip_record()
        attack_details4 = json.loads(banned_ip_record_4.attack_details)
        self.assertEqual(attack_details4['127.0.0.1']['count'], 3)

        BlockedIP.delete_table()

    def test_save_attacked_service_success(self):
        if not AttackedService.exists():
            AttackedService.create_table(wait=True)

        attacked_protocol_record = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record.service_name, 'Company Wordpress System')
        self.assertEqual(attacked_protocol_record.count, 1)

        attacked_protocol_record_2 = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record_2.service_name, 'Company Wordpress System')
        self.assertEqual(attacked_protocol_record_2.count, 2)

        attacked_protocol_record_3 = self.recorder2.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record_3.service_name, 'Back office service')
        self.assertEqual(attacked_protocol_record_3.count, 1)

        AttackedService.delete_table()

    def test_save_blocked_country_success(self):
        if not BlockedCountry.exists():
            BlockedCountry.create_table(wait=True)

        blocked_country_record = self.recorder.save_blocked_country_record()
        self.assertEqual(blocked_country_record.country_code, 'TH')
        self.assertEqual(blocked_country_record.country_name, 'Thailand')
        self.assertEqual(blocked_country_record.count, 1)

        self.recorder = StatsRecorder(self.attack_data2)
        blocked_country_record2 = self.recorder.save_blocked_country_record()
        self.assertEqual(blocked_country_record2.country_code, 'RU')
        self.assertEqual(blocked_country_record2.country_name, 'Russia')
        self.assertEqual(blocked_country_record2.count, 1)

        BlockedCountry.delete_table()