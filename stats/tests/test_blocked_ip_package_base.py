from django.test import SimpleTestCase
from django.conf import settings
from stats.models import BlockedIP
from stats.packages.blocked_ip import BlockedIPPackageBuilder
import time


class TestBlockedIPPackageBase(SimpleTestCase):
    def setUp(self):
        if not BlockedIP.exists():
            BlockedIP.create_table()
            time.sleep(settings.TESTING_SLEEP_TIME)
        attack_details = """
        [{{"ip":"127.0.0.1","service_name":"Company Wordpress System","protocol":"http","port":"80","count":1000,"last_seen":"2014-09-27T08:49:28.556775+0000"}}]
        """
        self.item1 = BlockedIP(lat_lon = "37.419200897216797,-122.05740356445312",
                          attack_details= attack_details,
                          country='US',
                          geo_location='CA, United States'
                          )
        self.item1.save()
        self.blocked_ips_builder = BlockedIPPackageBuilder()

    def tearDown(self):
        BlockedIP.delete_table()
        time.sleep(settings.TESTING_SLEEP_TIME)
