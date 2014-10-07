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

                               longitude=-122.05740356445312,
                               latitude=37.419200897216797,
                               country='US',
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
        self.assertIn('"protocol": "http"', content)
        self.assertIn('"port": "80"', content)
        self.assertIn('"longitude": -122.05740356445312', content)
        self.assertIn('"latitude": 37.4192', content)
        self.assertIn('"country": "US"', content)
        self.assertIn('"geo_location": "CA, United States"', content)
        self.assertIn('"count": 1000', content)
        self.assertIn('"last_seen": "Sep 27, 2014 08:49:28 +0000"', content)
        self.assertIn('{', content)
        self.assertIn('}', content)
        self.assertNotIn("category", content)

    def test_render_all_objects(self):
        content = self.blocked_ips_builder.render_all_objects()
        self.assertIn('"blocked_ip": "72.14.20.99"', content)
        self.assertIn('"service_name": "Company Wordpress System"', content)
        self.assertIn('"protocol": "http"', content)
        self.assertIn('"port": "80"', content)
        self.assertIn('"longitude": -122.05740356445312', content)
        self.assertIn('"latitude": 37.4192', content)
        self.assertIn('"country": "US"', content)
        self.assertIn('"geo_location": "CA, United States"', content)
        self.assertIn('"count": 1000', content)
        self.assertIn('"last_seen": "Sep 27, 2014 08:49:28 +0000"', content)
        self.assertIn('{', content)
        self.assertIn('}', content)
        self.assertNotIn("category", content)
        self.assertNotEqual(",", content[-1])

    def test_render_javascript(self):
        content = self.blocked_ips_builder.render_as_javascript()
        self.assertIn('var blocked_ips = [', content)
        self.assertIn('];', content)