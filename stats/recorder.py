from stats.models import BlockedIP, AttackedService, BlockedCountry
from attack.models import Attack
from pynamodb.connection import Connection
from django.utils.timezone import get_current_timezone
from django.conf import settings
from datetime import datetime
import json


class AttackDetailsRecorder(object):

    def __init__(self, attack_details):
        if attack_details:
            self.records = json.loads(attack_details)
        else:
            self.records = {'count': 0}

    def get_each_attack_template(self):
        return """
        {{
        "service_name":"{service_name}",
        "protocol":"{protocol}",
        "port":"{port}",
        "count":{count},
        "last_seen":"{last_seen}"
        }}
        """

    def build_attack_record_as_dict(self, data):
        existing_record = self.records.get(data['attacker_ip'], {})
        attack_details_dict = data.copy()
        attack_details_dict['count'] = existing_record.get(u'count', 0)+1
        attack_details_dict['last_seen'] = unicode(datetime.now(tz=get_current_timezone()))
        return json.loads(self.get_each_attack_template().format(**attack_details_dict) )

    def update_to_records(self, ip, attack_details):
        self.records[ip] = attack_details
        return self.records

    def dump_to_json(self):
        return json.dumps(self.records)

    def update_attack_record(self, data):
        new_attack = self.build_attack_record_as_dict(data)
        self.update_to_records(data['attacker_ip'], new_attack)
        return self.dump_to_json()


class StatsRecorder(object):

    def __init__(self, data):
        self.data = data
        self.ip = self.data['attacker_ip']
        self.connection = Connection(host=settings.DYNAMODB_HOST, region=settings.DYNAMODB_REGION)
        self.is_new_ip = self.check_new_ip()

    def trigger_counter(self, existing_record):
        if self.check_if_is_new_ip():
            if existing_record is None or (existing_record==[]):
                return 1
            count = existing_record.count + 1
            return count
        else:
            return existing_record.count

    def all_attribute_matched(self, item, query_data):
        if len(query_data.keys()) == 0:
            return item
        match = 0
        for query_parameter_key in query_data.keys():
            if getattr(item, query_parameter_key) == query_data[query_parameter_key]:
                match += 1
        if match == len(query_data.keys()) and (match != 0):
            return True
        return False

    def get_existing_record(self, model, hash_key, query_data={}):
        existing_blocked_ip = model.query(hash_key, **query_data)
        try:
            for item in existing_blocked_ip:
                if query_data == {}:
                    return item
                if self.all_attribute_matched(item, query_data):
                    return item

        except TypeError, err:
            return None

    def save_blocked_ip_record(self):
        lat_lon_string = "{latitude},{longitude}".format(**self.data)
        existing_record_response_dict = self.connection.query(settings.STATS_BLOCKED_IP_TABLE_NAME, lat_lon_string)

        if existing_record_response_dict['Count'] == 0:
            existing_attack_details = None
        else:
            existing_attack_details = existing_record_response_dict['Items'][0]['attack_details']['S']
        new_attack_details = AttackDetailsRecorder(existing_attack_details).update_attack_record(self.data)

        # self.blocked_ip = BlockedIP(
        #     lat_lon=lat_lon_string,
        #     attack_details=new_attack_details,
        #     country=self.data['country'],
        #     geo_location=self.data['geo_location'],
        # )
        # self.blocked_ip.save()
        new_data = dict(
            attack_details=new_attack_details,
            country=self.data['country'],
            geo_location=self.data['geo_location'],
        )
        self.connection.put_item(settings.STATS_BLOCKED_IP_TABLE_NAME, lat_lon_string,
                                     attributes=new_data)
        return self.blocked_ip

    def save_attacked_service_record(self):
        existing_record_response_dict = self.connection.query(settings.STATS_ATTACKED_SERVICE_TABLE_NAME, self.data['service_name'])
        if existing_record_response_dict['Count'] == 0:
            self.attacked_service = AttackedService(service_name=self.data['service_name'], count=1)
            self.attacked_service.save()
            return self.attacked_service
        else:
            existing_record = existing_record_response_dict['Items'][0]
            if self.is_new_ip:
                new_count = int(existing_record['count']['N']) + 1
                new_data = existing_record.copy()
                new_data['count']['N'] = unicode(new_count)
                self.connection.put_item(settings.STATS_ATTACKED_SERVICE_TABLE_NAME, self.data['service_name'],
                                     attributes=new_data)

    def check_new_ip(self):
        existing_attack_response_dict = self.connection.query(settings.ATTACK_TABLE_NAME, self.ip)
        if existing_attack_response_dict['Count'] == 0:
            return True
        else:
            return False

    def save_blocked_country_record(self):
        existing_record_response_dict = self.connection.query(settings.STATS_BLOCKED_COUNTRY_TABLE_NAME, self.data['country'])
        if existing_record_response_dict['Count'] == 0:
            self.blocked_country = BlockedCountry(country_code=self.data['country'],
                                              country_name=self.data['country_name'],
                                              count=1)
            self.blocked_country.save()
            return self.blocked_country
        else:
            existing_record = existing_record_response_dict['Items'][0]
            if self.is_new_ip:
                new_count = int(existing_record['count']['N']) + 1
                new_data = existing_record.copy()
                new_data['count']['N'] = unicode(new_count)
                self.connection.put_item(settings.STATS_BLOCKED_COUNTRY_TABLE_NAME, self.data['country'],
                                     attributes=new_data)

