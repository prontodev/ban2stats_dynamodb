from django.test import SimpleTestCase
from attack.models import Attack
from django.utils.timezone import get_current_timezone
from datetime import datetime
class TestModel(SimpleTestCase):

    def test_simple_model_usage(self):
        now_timestamp = datetime.now(tz=get_current_timezone())

        Attack.create_table(wait=True)

        attack = Attack(attacker_ip='127.0.0.1',
                        service_name='company web server',
                        protocol='http',
                        port='80',

                        longitude='111.333333',
                        latitude='222.33333',
                        country='Thailand',
                        geo_location='Bangkok, Thailand',
                        timestmap=now_timestamp)
        attack.save()

        # self.assertEqual(Attack.batch_get('127.0.0.1').get('ItemCount'), 1)

        Attack.delete_table()