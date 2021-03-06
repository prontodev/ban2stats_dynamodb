from attack.recorder import AttackRecorder
from attack.models import Attack
from ban2stats.utils.tables import create_all, delete_all
from django.test import SimpleTestCase
from django.conf import settings
import time


class TestAttackRecord(SimpleTestCase):

    def tearDown(self):
        delete_all()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def setUp(self):
        create_all()
        self.attack_recorder = AttackRecorder()

    def test_get_geo_data(self):
        ip = '72.14.207.99'
        geo_details = self.attack_recorder.get_geo_data(ip=ip)
        self.assertEqual(self.attack_recorder.data['country'], u'US')
        self.assertEqual(self.attack_recorder.data['geo_location'], u'CA, United States')

    def test_get_geo_data_invalid_ip(self):
        ip = '127.8.8.8'
        self.assertRaisesMessage(ValueError, 'Cannot find Geo details for this IP 127.8.8.8',
                                 self.attack_recorder.get_geo_data, ip=ip )

    def test_record_timestamp(self):
        self.attack_recorder.record_timestamp()
        self.assertTrue(self.attack_recorder.data['timestamp'])

    def test_record_save(self):
        self.attack_recorder.set_data(attacker_ip='72.14.207.99',
                        service_name='company web server',
                        protocol='http',
                        port='80',)
        self.attack_recorder.get_geo_data()
        self.attack_recorder.record_timestamp()
        self.attack_recorder.save()

        attacks_from_db = Attack.query('72.14.207.99', timestamp=self.attack_recorder.data['timestamp'])
        counter = 0
        for item in attacks_from_db:
            self.assertEqual(item.service_name, 'company web server')
            counter += 1
        self.assertEqual(1, counter)

    def test_set_data_with_empty_values(self):
        self.assertRaisesMessage(ValueError, 'Required attacker_ip, service_name, protocol and port.', self.attack_recorder.set_data)