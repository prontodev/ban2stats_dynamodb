from stats.tests.test_blocked_ip_package_base import TestBlockedIPPackageBase
from django.conf import settings
from stats.models import BlockedIP
from stats.packages.blocked_ip import BlockedIPPackageBuilder
import time


class TestBlockedIPPackageMinimized(TestBlockedIPPackageBase):
    pass
