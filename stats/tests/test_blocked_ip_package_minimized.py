from stats.tests.test_blocked_ip_package_base import TestBlockedIPPackageBase
from django.conf import settings
from stats.models import BlockedIP
from stats.packages.blocked_ip_minimized import BlockedIPPackageBuilderMinimized
import json


class TestBlockedIPPackageMinimized(TestBlockedIPPackageBase):

    def setUp(self):
        super(TestBlockedIPPackageMinimized, self).setUp()
        self.builder = BlockedIPPackageBuilderMinimized()

    def test_render_all_objects(self):
        content = self.builder.render_all_objects_as_list()
        expected_content = '''[\n["37.419200897216797","-122.05740356445312","CA, United States",[["127.0.0.1","Company Wordpress System",1000,"2014-09-27T08:49:28.556775+0000"]]]\n]'''
        self.assertEqual(content, expected_content)

    def test_render_each_object(self):
        content = self.builder.render_each_object(self.item1)
        expected_content = expected_content = '''["37.419200897216797","-122.05740356445312","CA, United States",[["127.0.0.1","Company Wordpress System",1000,"2014-09-27T08:49:28.556775+0000"]]]'''
        self.assertEqual(content, expected_content)

    def test_render_all_attack_details(self):
        all_attack_details = '''{"127.0.0.1": {"service_name":"Company Wordpress System","protocol":"http","port":"80","count":1000,"last_seen":"2014-09-27T08:49:28.556775+0000"},
        "127.0.0.2":{"service_name":"HR Portal","protocol":"http","port":"80","count":888,"last_seen":"2014-08-07T08:49:28.556775+0000"}
        }'''
        content = self.builder.render_all_attack_details(all_attack_details)
        expected_content = '''["127.0.0.2","HR Portal",888,"2014-08-07T08:49:28.556775+0000"]'''
        self.assertTrue(expected_content in content)
        expected_content = '''["127.0.0.1","Company Wordpress System",1000,"2014-09-27T08:49:28.556775+0000"]'''
        self.assertTrue(expected_content in content)
        self.assertEqual(content[0:2], "[[")
        self.assertEqual(content[-2:], "]]")

    def test_render_each_attack_detail(self):
        each_attack_details = {"ip":"127.0.0.1","service_name":"Company Wordpress System","protocol":"http","port":"80","count":18,"last_seen":"2014-09-27T08:49:28.556775+0000"}
        content = self.builder.render_each_attack_details(each_attack_details)
        expected_string = '''["127.0.0.1","Company Wordpress System",18,"2014-09-27T08:49:28.556775+0000"]'''
        self.assertEqual(content, expected_string)