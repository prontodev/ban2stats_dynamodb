from django.test import SimpleTestCase
from stats.models import AttackedService, BlockedIP, BlockedCountry
import time


class TestGetStatsViews(SimpleTestCase):

    def test_view__no_data(self):
        response = self.client.get('/stats/')
        self.assertContains(response, 'var blocked_ip_count = ')
        self.assertContains(response, 'var blocked_countries = [')
        self.assertContains(response, 'var blocked_ips = [')
        self.assertContains(response, 'var attacked_services = [')

    def test_view__with_data(self):
        if not AttackedService.exists():
            AttackedService.create_table()
            time.sleep(1)
        item1 = AttackedService(key="Internal Wordpress System", count=32923)
        item1.save()
        if not BlockedIP.exists():
            time.sleep(1)
            BlockedIP.create_table()
        item2 = BlockedIP("blocked_ip_72.14.207.99",
                               key="72.14.20.99",
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
        item2.save()
        if not BlockedCountry.exists():
            time.sleep(1)
            BlockedCountry.create_table()
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
        self.assertContains(response, 'var blocked_ip_count = ')
        self.assertContains(response, 'var blocked_countries = [')
        self.assertContains(response, 'var blocked_ips = [')
        self.assertContains(response, 'var attacked_services = [')

        AttackedService.delete_table()
        BlockedCountry.delete_table()