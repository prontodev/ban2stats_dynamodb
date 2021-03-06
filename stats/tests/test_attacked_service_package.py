from django.test import SimpleTestCase
from django.conf import settings
from stats.views import AttackedServicePackageBuilder
from stats.packages.attacked_service import AttackedService
import time


class TestGetAttackedServiceStats(SimpleTestCase):

    def setUp(self):
        if not AttackedService.exists():
            AttackedService.create_table()
            time.sleep(settings.TESTING_SLEEP_TIME)
        self.item1 = AttackedService(service_name="Internal Wordpress System", count=32923)
        self.item1.save()
        AttackedService(service_name="Mail Server", count=300).save()
        AttackedService(service_name="Company Secured Server", count=127563).save()
        self.attacked_services = AttackedServicePackageBuilder()

    def tearDown(self):
        AttackedService.delete_table()
        time.sleep(settings.TESTING_SLEEP_TIME)

    def test_get_attacked_services(self):
        objects = self.attacked_services.get_objects()
        self.assertEqual(len(objects), 3)

    def test_render_each_object(self):
        content = self.attacked_services.render_each_object(self.item1)
        self.assertEqual(content, u'["Internal Wordpress System", 32923]')

    def test_render_all_objects(self):
        content = self.attacked_services.render_all_objects()
        expected_content = u'''["Internal Wordpress System", 32923]'''
        self.assertIn(expected_content, content)
        expected_content = u'''["Mail Server", 300]'''
        self.assertIn(expected_content, content)
        expected_content = u'''["Company Secured Server", 127563]'''
        self.assertIn(expected_content, content)
        self.assertNotEqual(",", content[-1])

    def test_render_javascript(self):
        content = self.attacked_services.render_as_javascript()
        expected_content = u'''["Internal Wordpress System", 32923]'''
        self.assertIn(expected_content, content)
        expected_content = u'''["Mail Server", 300]'''
        self.assertIn(expected_content, content)
        expected_content = u'''["Company Secured Server", 127563]'''
        self.assertIn(expected_content, content)
        expected_content = u'''"attacked_services": ['''
        self.assertIn(expected_content, content)
        expected_content = u''']'''
        self.assertIn(expected_content, content)