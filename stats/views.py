from django.http.response import HttpResponse
from stats.models import AttackedService


class AttackedServicePackage(object):

    def get_objects(self):
        attacked_services = AttackedService.scan(category="attacked_service", count__gt=0)
        self.attacked_services_list = []
        for item in attacked_services:
            self.attacked_services_list.append(item)
        return self.attacked_services_list

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
    content += AttackedServicePackage().render_as_javascript()
    return HttpResponse(content)
