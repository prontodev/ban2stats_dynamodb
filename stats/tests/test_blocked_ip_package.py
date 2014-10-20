from django.test import SimpleTestCase
from django.conf import settings
from stats.models import BlockedIP
from stats.packages.blocked_ip import BlockedIPPackageBuilder
import time


class TestBlockedIPPackage(SimpleTestCase):
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

    def test_get_objects(self):
        objects = self.blocked_ips_builder.get_objects()
        self.assertEqual(len(objects), 1)

    def test_render_each_object(self):
        content = self.blocked_ips_builder.render_each_object(self.item1)
        content = content.replace("\\","")
        self.assertIn('"ip":"72.14.20.99"', content)
        self.assertIn('"service_name":"Company Wordpress System"', content)
        self.assertIn('"protocol":"http"', content)
        self.assertIn('"port":"80"', content)
        self.assertIn('"longitude":"-122.05740356445312"', content)
        self.assertIn('"latitude":"37.419200897216797"', content)
        self.assertIn('"country":"US"', content)
        self.assertIn('"geo_location":"CA, United States"', content)
        self.assertIn('"count":1000', content)
        self.assertIn('"last_seen":"Sep 27, 2014 08:49:28 +0000"', content)
        self.assertIn('{', content)
        self.assertIn('}', content)

    def test_render_all_objects(self):
        content = self.blocked_ips_builder.render_all_objects()
        self.assertIn('"ip": "72.14.20.99"', content)
        self.assertIn('"service_name":"Company Wordpress System"', content)
        self.assertIn('"protocol":"http"', content)
        self.assertIn('"port": "80"', content)
        self.assertIn('"longitude": "-122.05740356445312"', content)
        self.assertIn('"latitude": "37.419200897216797"', content)
        self.assertIn('"country": "US"', content)
        self.assertIn('"geo_location": "CA, United States"', content)
        self.assertIn('"count": 1000', content)
        self.assertIn('"last_seen": "Sep 27, 2014 08:49:28 +0000"', content)
        self.assertIn('{', content)
        self.assertIn('}', content)
        self.assertNotEqual(",", content[-1])

    def test_render_javascript(self):
        content = self.blocked_ips_builder.render_as_javascript()
        self.assertIn('"blocked_ips": [', content)
        self.assertIn('],', content)
        self.assertIn('"blocked_ip_count": "1"', content)