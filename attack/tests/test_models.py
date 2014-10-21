from django.test import SimpleTestCase
from attack.models import Attack
from django.utils.timezone import get_current_timezone
from datetime import datetime
import time
from pynamodb.exceptions import TableDoesNotExist
from django.conf import settings


class TestModel(SimpleTestCase):

    def tearDown(self):
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_simple_model_usage(self):
        now_timestamp = datetime.now(tz=get_current_timezone())

        try:
            Attack.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'
            Attack.create_table(wait=True)

        attack = Attack(attacker_ip='127.0.0.1',
                        service_name='company web server',
                        protocol='http',
                        port='80',

                        longitude="111.333333",
                        latitude="222.33333",
                        country='TH',
                        geo_location='Bangkok, Thailand',
                        timestamp=now_timestamp)
        attack.save()
        Attack.delete_table()

    def test_save_attack_fail(self):
        Attack.create_table(wait=True)
        attack = Attack()
        self.assertRaisesMessage(ValueError, "Attribute 'attacker_ip' cannot be None", attack.save)
        Attack.delete_table()