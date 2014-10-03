from django.test import SimpleTestCase
import time
from stats.recorder import StatsRecorder


class TestStatsRecord(SimpleTestCase):

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