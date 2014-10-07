from django.test import SimpleTestCase
from stats.models import BlockedIP
from stats.views import BlockedIPPackageBuilder
import time


class TestBlockedIPPackage(SimpleTestCase):
    def setUp(self):
        if not BlockedIP.exists():
            BlockedIP.create_table()
            time.sleep(1)
        self.item1 = BlockedIP("72.14.20.99",
                               category="blocked_ip_72.14.207.99",
                               service_name='Company Wordpress System',
                               protocol='http',
                               port='80',

                               longitude='111.333333',
                               latitude='222.33333',
                               country='TH',
                               geo_location='CA, United States',

                               count=1000,
                               last_seen='2014-09-27T08:49:28.556775+0000'
                               )
        self.item1.save()
        self.blocked_ips = BlockedIPPackageBuilder()

    def test_get_objects(self):
        objects = self.blocked_ips.get_objects()
        self.assertEqual(len(objects), 1)