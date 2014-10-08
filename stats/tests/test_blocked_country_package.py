from django.test import SimpleTestCase
from stats.models import BlockedCountry
from stats.views import BlockedCountryPackageBuilder
import time


class TestBlockedCountryPackageBuilder(SimpleTestCase):

    def setUp(self):
        self.builder = BlockedCountryPackageBuilder()
        if not BlockedCountry.exists():
            BlockedCountry.create_table()
            time.sleep(1)
        self.item1 = BlockedCountry("blocked_country", key='US', country_name='United States', count=22)
        self.item1.save()

    def tearDown(self):
        BlockedCountry.delete_table()
        time.sleep(1)

    def test_get_objects(self):
        objects = self.builder.get_objects()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].category, "blocked_country")

    # def