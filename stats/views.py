from django.http.response import HttpResponse
from pynamodb.exceptions import ScanError, QueryError
from stats.models import AttackedService, BlockedIP, BlockedCountry
import json
from dateutil.parser import parse


class PackageBuilder(object):

    def put_objects_to_list(self, objects):
        object_list = []
        try:
            for object in objects:
                object_list.append(object)
        except ScanError:
            pass
        except QueryError:
            pass
        return object_list

    def render_all_objects(self):
        all_rendered_object = []
        for each_object in self.get_objects():
            all_rendered_object.append(self.render_each_object(each_object))
        return ",\n".join(all_rendered_object)

    def render_all_objects_as_list(self):
        template = """[\n{0}\n]"""
        return template.format(self.render_all_objects())


class AttackedServicePackageBuilder(PackageBuilder):

    def get_objects(self):
        if not AttackedService.exists():
            return []
        attacked_services = AttackedService.scan(count__gt=0)
        return self.put_objects_to_list(attacked_services)

    def render_each_object(self, object):
        return u"""["{0}", {1}]""".format(object.service_name, object.count)

    def render_as_javascript(self):
        template = """
        "attacked_services": {0}"""
        return template.format(self.render_all_objects_as_list())


class BlockedIPPackageBuilder(PackageBuilder):

    def __init__(self):
        self.objects = []

    def get_objects(self):
        if not BlockedIP.exists():
            return []
        blocked_ip_objects = BlockedIP.scan(category__begins_with='blocked_ip_')
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
        output_dict['blocked_ip'] = output_dict.pop('key')
        output_dict.pop('category')
        output_dict['last_seen'] = self.format_last_seen_string(output_dict['last_seen'])
        return json.dumps(output_dict)

    def objects_count_as_string(self, number):
        return "{:,}".format(number)

    def render_as_javascript(self):
        template = """
        "blocked_ips": {0},\n
        "blocked_ip_count": "{1}"
        """
        return template.format(self.render_all_objects_as_list(), self.objects_count_as_string(len(self.objects)))


class BlockedCountryPackageBuilder(PackageBuilder):

    def get_top_5_objects(self):
        if not BlockedCountry.exists():
            return []
        try:
            blocked_country_objects = BlockedCountry.scan(limit=5, index='count_index', scan_index_forward=False)
        except ValueError:
            blocked_country_objects = BlockedCountry.count_index.query(limit=5, scan_index_forward=False)

        objects_as_list = self.put_objects_to_list(blocked_country_objects)
        if len(objects_as_list) < 5:
            return objects_as_list
        return objects_as_list[:5]

    def get_objects(self):
        return self.get_top_5_objects()

    def render_each_object(self, object):
        count_as_string = "{:,}".format(object.count)
        data_dict = dict(country_name=object.country_name, count=count_as_string)
        return json.dumps(data_dict)

    def render_as_javascript(self):
        template = """
        "blocked_countries": {0}"""
        return template.format(self.render_all_objects_as_list())


def get_stats(request):
    content = "{"
    content += '\n'
    content += BlockedIPPackageBuilder().render_as_javascript()
    content += ",\n"
    content += AttackedServicePackageBuilder().render_as_javascript()
    content += ",\n"
    content += BlockedCountryPackageBuilder().render_as_javascript()
    content += "\n}"
    response = HttpResponse(content, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response
