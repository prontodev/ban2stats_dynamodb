from attack.models import Attack
from django.contrib.gis.geoip import GeoIP


class AttackRecorder(object):

    def __init__(self, model=Attack):
        self.model = model
        if not self.model.exists():
            self.model.create_table(wait=True)

        self.geo_details = None

    def new_attack(self):
        self.attack = self.model()
        return self.attack

    def get_geo_details(self, ip=None):
        geo_ip = GeoIP()
        self.geo_details = geo_ip.city(ip)
        return self.geo_details