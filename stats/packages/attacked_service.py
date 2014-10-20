from stats.packages.base import PackageBuilder
from stats.models import AttackedService


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