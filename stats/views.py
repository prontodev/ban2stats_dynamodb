from django.http.response import HttpResponse
from stats.models import AttackedService, BlockedIP
from pynamodb.exceptions import ScanError
import json
from dateutil.parser import parse


class PackageBuilder(object):

    def put_objects_to_list(self, objects):
        object_list = []
        for object in objects:
            object_list.append(object)
        return object_list

    def render_all_objects(self):
        all_rendered_object = []
        for each_object in self.get_objects():
            all_rendered_object.append(self.render_each_object(each_object))
        return ",\n".join(all_rendered_object)


class AttackedServicePackageBuilder(PackageBuilder):

    def get_objects(self):
        if not AttackedService.exists():
            return []
        attacked_services = AttackedService.scan(category="attacked_service", count__gt=0)
        return self.put_objects_to_list(attacked_services)

    def render_each_object(self, object):
        return u"""["{0}", {1}]""".format(object.key, object.count)

    def render_as_javascript(self):
        template = """
        var attacked_services = [\r{0}\r
        ];"""
        return template.format(self.render_all_objects())


class BlockedIPPackageBuilder(PackageBuilder):

    def get_objects(self):
        if not BlockedIP.exists():
            return []
        blocked_ip_objects = BlockedIP.scan(category__begins_with='blocked_ip_')
        blocked_ip_list = self.put_objects_to_list(blocked_ip_objects)
        return blocked_ip_list

    def format_last_seen_string(self, last_seen_raw):
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

    def render_as_javascript(self):
        template = """
        var blocked_ips = [\r{0}\r
        ];"""
        return template.format(self.render_all_objects())


class BlockedCountryPackageBuilder(PackageBuilder):
    pass

def get_stats(request):
    if not AttackedService.exists():
        AttackedService.create_table()
    item1 = AttackedService(key="Internal Wordpress System", count=32923)
    item1.save()
    if not BlockedIP.exists():
        BlockedIP.create_table()
    item2 = BlockedIP("72.14.20.99",
                           category="blocked_ip_72.14.207.99",
                           service_name='Company Wordpress System',
                           protocol='http',
                           port='80',

                           longitude=-122.05740356445312,
                           latitude=37.419200897216797,
                           country='US',
                           geo_location='CA, United States',

                           count=1000,
                           last_seen='2014-09-27T08:49:28.556775+0000'
                           )
    item2.save()


    content = """
    var blocked_ip_count = "2,777,000";
    var blocked_countries = [
        { country_name: "United States", count: "3,000"},
        { country_name:"Thailand", count : "2,999"},
        { country_name:"Singapore", count: "1,000"},
        { country_name:"Malaysia", count: "300"},
        { country_name:"Indonesia", count: "11"}
    ]

    """
    content += "\n"
    content += BlockedIPPackageBuilder().render_as_javascript()
    content += "\n"
    content += AttackedServicePackageBuilder().render_as_javascript()
    item1.delete()
    item2.delete()
    return HttpResponse(content)
