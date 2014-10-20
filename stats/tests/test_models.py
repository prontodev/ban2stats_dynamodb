from django.test import SimpleTestCase
from django.conf import settings
from stats.models import BlockedIP, AttackedService, BlockedCountry
import time
from django.utils.timezone import get_current_timezone
from datetime import datetime
from pynamodb.exceptions import TableDoesNotExist


class TestModel(SimpleTestCase):

    def tearDown(self):
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_BlockedIP_simple_model_usage(self):
        now_timestamp = unicode(datetime.now(tz=get_current_timezone()))

        try:
            BlockedIP.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'
            BlockedIP.create_table(wait=True)

        attack_details = """
        [{{"ip":"127.0.0.1","service_name":"company web server","protocol":"http","port":"80","count":0,"last_seen":"{0}"}}]
        """.format(now_timestamp)
        blocked_ip = BlockedIP(
                        lat_lon = "222.33333,111.333333",
                        attack_details= attack_details,
                        country='TH',
                        geo_location='Bangkok, Thailand')
        blocked_ip.save()
        BlockedIP.delete_table()

    def test_attacked_service_model(self):
        try:
            AttackedService.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'
            AttackedService.create_table(wait=True)

        attacked_protocol = AttackedService(
                        service_name='Wordpress HTTP',
                        count=1)
        attacked_protocol.save()
        AttackedService.delete_table()

    def test_blocked_country_model(self):

        try:
            BlockedCountry.create_table(wait=True)
        except TableDoesNotExist:
            #It happens when create_table api doesn't finished within `timeout`.
            print 'Raised TableDoesNotExist'
            BlockedCountry.create_table(wait=True)

        blocked_country = BlockedCountry(
                        country_code='TH',
                        country_name='Thailand',
                        count=1)
        blocked_country.save()
        BlockedCountry.delete_table()