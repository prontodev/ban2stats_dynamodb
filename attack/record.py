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
        self.data = {}

    def set_data(self, attacker_ip=None, service_name=None, protocol=None, port=None):
        self.data['attacker_ip'] = attacker_ip
        self.data['service_name'] = service_name
        self.data['protocol'] = protocol
        self.data['port'] = port

    def get_geo_data(self, ip=None):
        if not ip: ip=self.data['attacker_ip']
        geo_ip = GeoIP()
        self.geo_details = geo_ip.city(ip)

        self.data['country'] = self.geo_details['country_code']
        self.data['latitude'] = unicode(self.geo_details['latitude'])
        self.data['longitude'] = unicode(self.geo_details['longitude'])

        self.data['geo_location'] = ', '.join([self.geo_details['region'], self.geo_details['country_name']])

    def record_timestamp(self):
        now_timestamp = datetime.now(tz=get_current_timezone())
        self.data['timestamp'] = now_timestamp

    def save(self):
        attack = self.model(**self.data)
        attack.save()

    def delete_table(self):
        self.model.delete_table()