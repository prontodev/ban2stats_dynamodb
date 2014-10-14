from stats.models import BlockedIP, AttackedService, BlockedCountry
from django.utils.timezone import get_current_timezone
from datetime import datetime


class StatsRecorder(object):

    def __init__(self, data):
        self.data = data
        self.ip = self.data['attacker_ip']

        if not BlockedIP.exists():
            BlockedIP.create_table(wait=True)

    def trigger_counter(self, existing_record, query_data={}):
        if existing_record is None or (existing_record==[]): return 1
        try:
            existing_record = self.get_right_record(existing_record, query_data)
        except IndexError, err:
            return 1
        if existing_record is None:
            return 1
        count = existing_record.count + 1
        return count

    def get_right_record(self, existing_record, query_data={}):
        for record in existing_record:
            match = 0
            for query_parameter_key in query_data.keys():
                if getattr(record, query_parameter_key) == query_data[query_parameter_key]:
                    match += 1
            if match == len(query_data.keys()) and (match != 0):
                return record

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
        query_data = dict(key=self.ip, service_name=self.data['service_name'])
        existing_record = self.get_existing_record(category,
                                                   query_data=query_data)
        count = self.trigger_counter(existing_record, query_data)
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

    def save_attacked_service_record(self):
        existing_record = self.get_existing_record('attacked_service', dict(category=self.data['service_name']))
        count = self.trigger_counter(existing_record, {'key': self.data['service_name']})
        self.attacked_service = AttackedService(key=self.data['service_name'], count=count)
        self.attacked_service.save()
        return self.attacked_service

    def save_blocked_country_record(self):
        query_data = dict(key=self.data['country'])
        existing_record = self.get_existing_record('blocked_country', query_data)
        count = self.trigger_counter(existing_record, query_data=query_data)
        self.blocked_country = BlockedCountry(key=self.data['country'],
                                              country_name=self.data['country_name'],
                                              count=count)
        self.blocked_country.save()
        return self.blocked_country

    def delete_table(self):
        BlockedIP.delete_table()