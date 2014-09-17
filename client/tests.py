from unittest import TestCase
from webservice_client import BAN2STATSHandler


class ClientTest(TestCase):

    def test_initiation(self):
        handler = BAN2STATSHandler()