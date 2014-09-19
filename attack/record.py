from attack.models import Attack
from django.contrib.gis.geoip import GeoIP
from django.utils.timezone import get_current_timezone
from datetime import datetime


class AttackRecorder(object):

    def __init__(self, model=Attack):
        self.model = model
        if not self.model.exists():
            self.model.create_table(wait=True)

        self.geo_details = None

    def new_attack(self):
        self.attack = self.model()
        return self.attack

    def set_data(self, attacker_ip=None, service_name=None, protocol=None, port=None):
        self.attack.attacker_ip = attacker_ip
        self.attack.service_name = service_name
        self.attack.protocol = protocol
        self.attack.port = port

    def get_geo_data(self, ip=None):
        if not ip: ip=self.attack.attacker_ip
        geo_ip = GeoIP()
        self.geo_details = geo_ip.city(ip)

        self.attack.country = self.geo_details['country_code']
        self.attack.latitude = self.geo_details['latitude']
        self.attack.longitude = self.geo_details['longitude']

        self.attack.geo_location = ', '.join([self.geo_details['region'], self.geo_details['country_name']])

    def record_timestamp(self):
        now_timestamp = datetime.now(tz=get_current_timezone())
        self.attack.timestmap = now_timestamp

    def save(self):
        self.attack.save()