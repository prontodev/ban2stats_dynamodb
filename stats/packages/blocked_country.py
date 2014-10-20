from stats.packages.base import PackageBuilder
from stats.models import BlockedCountry
import json


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

