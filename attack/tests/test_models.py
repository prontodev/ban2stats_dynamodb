from django.test import SimpleTestCase
from attack.models import Attack
from django.utils.timezone import get_current_timezone
from datetime import datetime


class AttackForTesting(Attack):

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'AttackTest'
        host = 'http://localhost:4567'


class TestModel(SimpleTestCase):

    def test_simple_model_usage(self):
        now_timestamp = datetime.now(tz=get_current_timezone())

        AttackForTesting.create_table(wait=True)

        attack = AttackForTesting(attacker_ip='127.0.0.1',
                        service_name='company web server',
                        protocol='http',
                        port='80',

                        longitude='111.333333',
                        latitude='222.33333',
                        country='TH',
                        geo_location='Bangkok, Thailand',
                        timestmap=now_timestamp)
        attack.save()

        AttackForTesting.delete_table()