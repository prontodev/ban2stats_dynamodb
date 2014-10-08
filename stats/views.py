from django.http.response import HttpResponse
from stats.models import AttackedService, BlockedIP, BlockedCountry
import json
from dateutil.parser import parse


class PackageBuilder(object):

    def put_objects_to_list(self, objects):
        object_list = []
        try:
            for object in objects:
                object_list.append(object)
            return object_list
        except ValueError, err:
            return []

    def render_all_objects(self):
        all_rendered_object = []
        for each_object in self.get_objects():
            all_rendered_object.append(self.render_each_object(each_object))
        return ",\n".join(all_rendered_object)

    def render_all_objects_as_list(self):
        template = """[\r{0}\r];"""
        return template.format(self.render_all_objects())


class AttackedServicePackageBuilder(PackageBuilder):

    def get_objects(self):
        if not AttackedService.exists():
            return []
        attacked_services = AttackedService.query("attacked_service", count__gt=0)
        return self.put_objects_to_list(attacked_services)

    def render_each_object(self, object):
        return u"""["{0}", {1}]""".format(object.key, object.count)

    def render_as_javascript(self):
        template = """
        var attacked_services = {0};"""
        return template.format(self.render_all_objects_as_list())


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
        var blocked_ips = {0};"""
        return template.format(self.render_all_objects_as_list())


class BlockedCountryPackageBuilder(PackageBuilder):

    def get_top_5_objects(self):
        if not BlockedCountry.exists():
            return []
        blocked_country_objects = BlockedCountry.count_index.query('blocked_country', limit=5, scan_index_forward=False, Count=True)
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
        var blocked_countries = {0};"""
        return template.format(self.render_all_objects_as_list())


def get_stats(request):
    import time
    if not AttackedService.exists():
        AttackedService.create_table()
        time.sleep(1)
    item1 = AttackedService(key="Internal Wordpress System", count=32923)
    item1.save()
    if not BlockedIP.exists():
        time.sleep(1)
        BlockedIP.create_table()
    item2 = BlockedIP("blocked_ip_72.14.207.99",
                           key="72.14.20.99",
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
    if not BlockedCountry.exists():
        time.sleep(1)
        BlockedCountry.create_table()
    item1 = BlockedCountry("blocked_country", key='US', country_name='United States', count=22)
    item1.save()
    item2 = BlockedCountry("blocked_country", key='TH', country_name='Thailand', count=3000)
    item2.save()
    item3 = BlockedCountry("blocked_country", key='SG', country_name='Singapore', count=12094)
    item3.save()
    item4 = BlockedCountry("blocked_country", key='AL', country_name='Albania', count=3)
    item4.save()
    item5 = BlockedCountry("blocked_country", key='MA', country_name='Morocco', count=34123)
    item5.save()
    item6 = BlockedCountry("blocked_country", key='PE', country_name='Peru', count=50)
    item6.save()


    content = """
    var blocked_ip_count = "2,777,000";

    """
    content += "\n"
    content += BlockedCountryPackageBuilder().render_as_javascript()
    content += "\n"
    content += BlockedIPPackageBuilder().render_as_javascript()
    content += "\n"
    content += AttackedServicePackageBuilder().render_as_javascript()
    item1.delete()
    item2.delete()
    return HttpResponse(content)
