from django.http.response import HttpResponse
from stats.models import AttackedService, BlockedIP


class PackageBuilder(object):

    def put_objects_to_list(self, objects):
        object_list = []
        for object in objects:
            object_list.append(object)
        return object_list


class AttackedServicePackageBuilder(PackageBuilder):

    def get_objects(self):
        attacked_services = AttackedService.scan(category="attacked_service", count__gt=0)
        return self.put_objects_to_list(attacked_services)

    def render_each_object(self, object):
        return u"""["{0}", {1}]""".format(object.key, object.count)

    def render_all_objects(self):
        all_rendered_object = []
        for each_object in self.get_objects():
            all_rendered_object.append(self.render_each_object(each_object))
        return ",\n".join(all_rendered_object)

    def render_as_javascript(self):
        template = """
        var attacked_services = [\r{0}\r
        ];"""
        return template.format(self.render_all_objects())


class BlockedIPPackageBuilder(PackageBuilder):

    def get_objects(self):
        blocked_ip_objects = BlockedIP.scan(category__begins_with='blocked_ip_')
        blocked_ip_list = self.put_objects_to_list(blocked_ip_objects)
        return blocked_ip_list


def get_stats(request):
    content = """
    var blocked_ip_count = "2,777,000";
    var blocked_countries = [
        { country_name: "United States", count: "3,000"},
        { country_name:"Thailand", count : "2,999"},
        { country_name:"Singapore", count: "1,000"},
        { country_name:"Malaysia", count: "300"},
        { country_name:"Indonesia", count: "11"}
    ]
    var pins = [
        { blocked_ip: "72.14.207.99", service_name: "Internal Wordpress System", protocol: "http", port: "80",
          count: "30", last_seen: "Sep 27, 2014 12:33",
          latitude: 37.419200897216797, longitude: "-122.05740356445312",
          geo_location: "CA, United States"
        }
    ];
    """
    content += AttackedServicePackageBuilder().render_as_javascript()
    return HttpResponse(content)
