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
        self.item2 = BlockedCountry("blocked_country", key='TH', country_name='Thailand', count=3000)
        self.item2.save()
        self.item3 = BlockedCountry("blocked_country", key='SG', country_name='Singapore', count=12094)
        self.item3.save()
        self.item4 = BlockedCountry("blocked_country", key='AL', country_name='Albania', count=3)
        self.item4.save()
        self.item5 = BlockedCountry("blocked_country", key='MA', country_name='Morocco', count=34123)
        self.item5.save()
        self.item6 = BlockedCountry("blocked_country", key='PE', country_name='Peru', count=50)
        self.item6.save()

    def tearDown(self):
        BlockedCountry.delete_table()
        time.sleep(1)

    def test_get_top_5(self):
        objects = self.builder.get_top_5_objects()
        self.assertEqual(len(objects), 5)
        self.assertEqual(objects[0].category, "blocked_country")
        self.assertEqual(objects[0].count, 34123)
        self.assertEqual(objects[1].count, 12094)
        self.assertEqual(objects[2].count, 3000)
        self.assertEqual(objects[3].count, 50)
        self.assertEqual(objects[4].count, 22)