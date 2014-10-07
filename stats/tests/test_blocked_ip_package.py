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

                               longitude=111.333333,
                               latitude=222.33333,
                               country='TH',
                               geo_location='CA, United States',

                               count=1000,
                               last_seen='2014-09-27T08:49:28.556775+0000'
                               )
        self.item1.save()
        self.blocked_ips_builder = BlockedIPPackageBuilder()

    def test_get_objects(self):
        objects = self.blocked_ips_builder.get_objects()
        self.assertEqual(len(objects), 1)

    def test_render_each_object(self):
        content = self.blocked_ips_builder.render_each_object(self.item1)
        self.assertIn('"blocked_ip": "72.14.20.99"', content)
        self.assertIn('"service_name": "Company Wordpress System"', content)
        self.assertIn('"longitude": 111.333333', content)
        self.assertIn('"geo_location": "CA, United States"', content)
        self.assertIn('"count": 1000', content)
        self.assertIn('"last_seen": "Sep 27, 2014 08:49:28 +0000"', content)
        self.assertNotIn("category", content)