from stats.packages.base import PackageBuilder
from stats.models import BlockedCountry
import json


class BlockedCountryPackageBuilder(PackageBuilder):

    def get_top_5_objects(self):
        if not BlockedCountry.exists():
            return []
        blocked_country_objects = BlockedCountry.scan()
        sort_filter = lambda item: item.count
        objects_as_list = sorted(blocked_country_objects, key=sort_filter, reverse=True)
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

