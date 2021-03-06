from stats.packages.base import PackageBuilder
from stats.models import BlockedIP
from dateutil.parser import parse
import json


class BlockedIPPackageBuilderMinimized(PackageBuilder):

    def __init__(self):
        self.objects = []

    def get_objects(self):
        if not BlockedIP.exists():
            return []
        blocked_ip_objects = BlockedIP.scan()
        blocked_ip_list = self.put_objects_to_list(blocked_ip_objects)
        self.objects = blocked_ip_list
        return blocked_ip_list

    def format_last_seen_string(self, last_seen_raw):
        if last_seen_raw is None:
            return 'n/a'
        last_seen_datetime = parse(last_seen_raw)
        return last_seen_datetime.strftime("%b %d, %Y %H:%M:%S %z")

    def render_each_object(self, object):
        latitude, longitude = object.lat_lon.split(',')
        data = {'latitude' : latitude, 'longitude': longitude}
        data['geo_location'] = object.geo_location
        data['list_of_attack_details_as_string'] = self.render_all_attack_details(object.attack_details)
        template = '''["{latitude}","{longitude}","{geo_location}",{list_of_attack_details_as_string}]'''
        output_string = template.format(**data)
        return output_string

    def render_all_attack_details(self, all_attack_details_as_string):
        all_attack_details_as_dict = json.loads(all_attack_details_as_string)
        output_list = []
        attack_details_without_count = all_attack_details_as_dict.copy()
        try:
            attack_details_without_count.pop(u'count')
        except KeyError:
            pass
        for ip, details in attack_details_without_count.items():
            data = {'ip': ip}
            data.update(details)
            output_list.append(self.render_each_attack_details(data))
        output_string = ",".join(output_list)
        output_string = "[{0}]".format(output_string)
        return output_string

    def render_each_attack_details(self, each_attack_details_as_dict):
        output_string = '''["{ip}","{service_name}",{count},"{last_seen}"]'''.format(**each_attack_details_as_dict)
        return output_string

    def objects_count_as_string(self, number):
        return "{:,}".format(number)

    def render_as_javascript(self):
        template = """
        "blocked_ips": {0},\n
        "blocked_ip_count": "{1}"
        """
        return template.format(self.render_all_objects_as_list(), self.objects_count_as_string(len(self.objects)))


