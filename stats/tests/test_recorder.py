from django.test import SimpleTestCase
import time
from stats.recorder import StatsRecorder


class TestStatsRecorder(SimpleTestCase):

    def test_save_stats_success(self):
        attack_data = dict(
            attacker_ip='127.0.0.1',
            service_name='company web server',
            protocol='http',
            port='80',

            longitude='111.333333',
            latitude='222.33333',
            country='TH',
            geo_location='Bangkok, Thailand'
        )
        recorder = StatsRecorder(attack_data)
        banned_ip_record = recorder.save_banned_ip_record()
        self.assertEqual(banned_ip_record.category, 'blocked_ip_127.0.0.1')
        self.assertEqual(banned_ip_record.key, '127.0.0.1')
        self.assertEqual(banned_ip_record.protocol, 'http')
        self.assertEqual(banned_ip_record.port, '80')
        self.assertEqual(banned_ip_record.service_name, 'company web server')
        self.assertEqual(banned_ip_record.longitude, '111.333333')
        self.assertEqual(banned_ip_record.latitude, '222.33333')
        self.assertEqual(banned_ip_record.geo_location, 'Bangkok, Thailand')

        self.assertEqual(banned_ip_record.count, 1)
        self.assertTrue(banned_ip_record.last_seen)

        banned_ip_record_2 = recorder.save_banned_ip_record()
        self.assertEqual(banned_ip_record_2.count, 2)

        recorder.delete_table()