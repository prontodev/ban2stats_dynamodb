from pynamodb.exceptions import ScanError, QueryError


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