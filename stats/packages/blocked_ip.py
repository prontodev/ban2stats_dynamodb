from stats.packages.base import PackageBuilder
from stats.models import BlockedIP
from dateutil.parser import parse
import json


class BlockedIPPackageBuilder(PackageBuilder):

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
        output_dict = dict()
        for item_key, item_value in object._get_attributes().iteritems():
            output_dict[item_key] = getattr(object, item_key)

        # output_dict['last_seen'] = self.format_last_seen_string(output_dict['last_seen'])
        return json.dumps(output_dict)

    def objects_count_as_string(self, number):
        return "{:,}".format(number)

    def render_as_javascript(self):
        template = """
        "blocked_ips": {0},\n
        "blocked_ip_count": "{1}"
        """
        return template.format(self.render_all_objects_as_list(), self.objects_count_as_string(len(self.objects)))
