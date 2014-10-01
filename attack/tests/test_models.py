from django.test import SimpleTestCase
from attack.models import Attack
from django.utils.timezone import get_current_timezone
from datetime import datetime
import time
from pynamodb.exceptions import TableDoesNotExist


class AttackForTesting(Attack):

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'AttackTest'
        region = 'ap-southeast-1'
        host = 'http://localhost:4567'


class TestModel(SimpleTestCase):

    def tearDown(self):
        time.sleep(1)

    def test_simple_model_usage(self):
        now_timestamp = datetime.now(tz=get_current_timezone())

        try:
            AttackForTesting.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'

        attack = AttackForTesting(attacker_ip='127.0.0.1',
                        service_name='company web server',
                        protocol='http',
                        port='80',

                        longitude='111.333333',
                        latitude='222.33333',
                        country='TH',
                        geo_location='Bangkok, Thailand',
                        timestamp=now_timestamp)
        attack.save()
        AttackForTesting.delete_table()

    def test_save_attack_fail(self):
        AttackForTesting.create_table(wait=True)
        attack = AttackForTesting()
        self.assertRaisesMessage(ValueError, "Attribute 'attacker_ip' cannot be None", attack.save)
        AttackForTesting.delete_table()