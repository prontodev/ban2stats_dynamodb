from django.test import SimpleTestCase
from django.conf import settings
from stats.models import AttackedService, BlockedIP, BlockedCountry
import time


class TestGetStatsViews(SimpleTestCase):

    def setUp(self):
        if not AttackedService.exists():
            AttackedService.create_table(wait=True)
            time.sleep(settings.TESTING_SLEEP_TIME)
        if not BlockedIP.exists():
            BlockedIP.create_table(wait=True)
            time.sleep(settings.TESTING_SLEEP_TIME)
        if not BlockedCountry.exists():
            BlockedCountry.create_table(wait=True)
            time.sleep(settings.TESTING_SLEEP_TIME)

    def tearDown(self):
        BlockedIP.delete_table()
        AttackedService.delete_table()
        BlockedCountry.delete_table()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_view__no_data(self):
        response = self.client.get('/stats/')
        self.assertContains(response, '"blocked_ip_count":')
        self.assertContains(response, '"blocked_countries": [')
        self.assertContains(response, '"blocked_ips": [')
        self.assertContains(response, '"attacked_services": [')

    def test_view__with_data(self):
        item1 = AttackedService(service_name="Internal Wordpress System", count=32923)
        item1.save()

        attack_details = """
        {"127.0.0.1":{"service_name":"Company Wordpress System","protocol":"http","port":"80","count":1000,"last_seen":"2014-09-27T08:49:28.556775+0000"}}
        """
        item2 = BlockedIP(lat_lon = "37.419200897216797,-122.05740356445312",
                          attack_details= attack_details,
                          country='US',
                          geo_location='CA, United States'
                          )
        item2.save()

        item1 = BlockedCountry("blocked_country", key='US', country_name='United States', count=22)
        item1.save()
        item2 = BlockedCountry("blocked_country", key='TH', country_name='Thailand', count=3000)
        item2.save()
        item3 = BlockedCountry("blocked_country", key='SG', country_name='Singapore', count=12094)
        item3.save()
        item4 = BlockedCountry("blocked_country", key='AL', country_name='Albania', count=3)
        item4.save()
        item5 = BlockedCountry("blocked_country", key='MA', country_name='Morocco', count=34123)
        item5.save()
        item6 = BlockedCountry("blocked_country", key='PE', country_name='Peru', count=50)
        item6.save()

        response = self.client.get('/stats/')
        self.assertContains(response, '"blocked_ip_count": ')
        self.assertContains(response, '"blocked_countries": [')
        self.assertContains(response, '"blocked_ips": [')
        self.assertContains(response, '"attacked_services": [')