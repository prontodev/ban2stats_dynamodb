from attack.models import Attack
from django.contrib.gis.geoip import GeoIP


class AttackRecorder(object):

    def __init__(self, model=Attack):
        self.model = model
        if not self.model.exists():
            self.model.create_table(wait=True)

    def new_attack(self):
        self.attack = self.model()
        return self.attack

    def get_geo_location(self, ip=None):
        geo_ip = GeoIP()
        geo_location = geo_ip.city(ip)
        return geo_location