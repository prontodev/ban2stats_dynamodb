from django.test import SimpleTestCase
from django.conf import settings
import time
import json
from stats.recorder import StatsRecorder
from ban2stats.utils.tables import create_all, delete_all
from stats.models import BlockedIP


class TestStatsRecorder(SimpleTestCase):

    def setUp(self):
        create_all()

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

        self.attack_data3 = dict(
            attacker_ip='127.0.0.3',
            service_name='HR Portal',
            protocol='http',
            port='9090',

            longitude="111.333333",
            latitude="222.33333",
            country='RU',
            country_name='Russia',
            geo_location='n/a, Russia'
        )
        self.recorder3 = StatsRecorder(self.attack_data3)

        self.attack_data4 = dict(
            attacker_ip='127.0.0.2',
            service_name='Call Center Portal',
            protocol='http',
            port='9090',

            longitude="555.6666",
            latitude="77.8888",
            country='RU',
            country_name='Russia',
            geo_location='n/a, Russia'
        )
        self.recorder4 = StatsRecorder(self.attack_data3)

    def tearDown(self):
        delete_all()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_save_banned_ip_success(self):

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

        attacked_protocol_record = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record.service_name, 'Company Wordpress System')
        self.assertEqual(attacked_protocol_record.count, 1)

        self.recorder.is_new_ip = False #mock
        attacked_protocol_record_2 = self.recorder.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record_2, None)
        attacked_protocol_record_from_db = self.recorder.connection.query(settings.STATS_ATTACKED_SERVICE_TABLE_NAME,
'Company Wordpress System')
        self.assertEqual(attacked_protocol_record_from_db['Count'], 1)
        self.assertEqual(attacked_protocol_record_from_db['Items'][0]['count']['N'],'1')
        self.assertEqual(attacked_protocol_record_from_db['Items'][0]['service_name']['S'],'Company Wordpress System')

        attacked_protocol_record_3 = self.recorder2.save_attacked_service_record()
        self.assertEqual(attacked_protocol_record_3.count, 1)
        self.assertEqual(attacked_protocol_record_3.service_name, 'Back office service')
        attacked_protocol_from_db3 = self.recorder2.connection.query(settings.STATS_ATTACKED_SERVICE_TABLE_NAME, 'Back office service')
        self.assertEqual(attacked_protocol_from_db3['Count'], 1)
        self.assertEqual(attacked_protocol_from_db3['Items'][0]['count']['N'], '1')
        self.assertEqual(attacked_protocol_from_db3['Items'][0]['service_name']['S'], 'Back office service')

    def test_save_blocked_country_success(self):

        blocked_country_record = self.recorder.save_blocked_country_record()
        self.assertEqual(blocked_country_record.country_code, 'TH')
        self.assertEqual(blocked_country_record.country_name, 'Thailand')
        self.assertEqual(blocked_country_record.count, 1)

        blocked_country_record2 = self.recorder2.save_blocked_country_record()
        self.assertEqual(blocked_country_record2.country_code, 'RU')
        self.assertEqual(blocked_country_record2.country_name, 'Russia')
        self.assertEqual(blocked_country_record2.count, 1)

        time.sleep(1)

        blocked_country_record3 = self.recorder3.save_blocked_country_record()
        self.assertEqual(blocked_country_record3, None)
        blocked_country_from_db3 = self.recorder3.connection.query(settings.STATS_BLOCKED_COUNTRY_TABLE_NAME, "RU")
        self.assertEqual(blocked_country_from_db3['Items'][0]['country_code']['S'], 'RU')
        self.assertEqual(blocked_country_from_db3['Items'][0]['country_name']['S'], 'Russia')
        self.assertEqual(blocked_country_from_db3['Items'][0]['count']['N'], '2')

        self.recorder4.is_new_ip = False #mock
        blocked_country_record4 = self.recorder4.save_blocked_country_record()
        self.assertEqual(blocked_country_record4, None)
        blocked_country_from_db4 = self.recorder4.connection.query(settings.STATS_BLOCKED_COUNTRY_TABLE_NAME, "RU")
        self.assertEqual(blocked_country_from_db4['Items'][0]['country_code']['S'], 'RU')
        self.assertEqual(blocked_country_from_db4['Items'][0]['country_name']['S'], 'Russia')
        self.assertEqual(blocked_country_from_db4['Items'][0]['count']['N'], '2')