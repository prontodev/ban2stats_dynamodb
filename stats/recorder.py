from stats.models import BlockedIP, AttackedProtocol, BlockedCountry
from django.utils.timezone import get_current_timezone
from datetime import datetime


class StatsRecorder(object):

    def __init__(self, data):
        self.data = data
        self.ip = self.data['attacker_ip']

        if not BlockedIP.exists():
            BlockedIP.create_table(wait=True)

    def trigger_counter(self, existing_record):
        if existing_record is None: return 0
        try:
            existing_record = existing_record[0]
        except IndexError, err:
            return 1
        count = existing_record.count + 1
        return count

    def get_existing_record(self, hash_key, query_data):
        existing_blocked_ip = BlockedIP.query(hash_key, **query_data)
        existing_records = []
        try:
            for item in existing_blocked_ip:
                existing_records.append(item)
        except TypeError, err:
            return None
        return existing_records

    def get_blocked_ip_category(self):
        category = 'blocked_ip_{0}'.format(self.ip)
        return category

    def save_banned_ip_record(self):
        category = self.get_blocked_ip_category()
        existing_record = self.get_existing_record(hash_key=self.ip,
                                                   query_data=dict(category=category,
                                                                   service_name=self.data['service_name']))
        count = self.trigger_counter(existing_record)
        last_seen = unicode(datetime.now(tz=get_current_timezone()))
        self.blocked_ip = BlockedIP(
            category=category,
            key=self.ip,
            service_name=self.data['service_name'],
            protocol=self.data['protocol'],
            port=self.data['port'],
            longitude=self.data['longitude'],
            latitude=self.data['latitude'],
            country=self.data['country'],
            geo_location=self.data['geo_location'],
            count=count,
            last_seen=last_seen,
        )
        self.blocked_ip.save()
        return self.blocked_ip

    def save_attacked_protocol_record(self):
        existing_record = self.get_existing_record(self.data['protocol'], dict(category='attacked_protocol'))
        count = self.trigger_counter(existing_record)
        self.attacked_protocol = AttackedProtocol(key=self.data['protocol'], count=count)
        self.attacked_protocol.save()
        return self.attacked_protocol

    def save_blocked_country_record(self):
        existing_record = self.get_existing_record(self.data['country'], dict(category='blocked_country'))
        count = self.trigger_counter(existing_record)
        self.blocked_country = BlockedCountry(key=self.data['country'],
                                              country_name=self.data['country_name'],
                                              count=count)
        self.blocked_country.save()
        print 'blocked country = ', self.blocked_country.country_name
        return self.blocked_country

    def delete_table(self):
        BlockedIP.delete_table()