from django.http.response import HttpResponse
from stats.packages.attacked_service import AttackedServicePackageBuilder
from stats.packages.blocked_ip_minimized import BlockedIPPackageBuilderMinimized
from stats.packages.blocked_country import BlockedCountryPackageBuilder


def get_stats(request):
    content = "{"
    content += '\n'
    content += BlockedIPPackageBuilderMinimized().render_as_javascript()
    content += ",\n"
    content += AttackedServicePackageBuilder().render_as_javascript()
    content += ",\n"
    content += BlockedCountryPackageBuilder().render_as_javascript()
    content += "\n}"
    return return_json_content(content)


def return_json_content(content):
    response = HttpResponse(content, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response


def get_attacked_services(request):
    content = AttackedServicePackageBuilder().render_all_objects_as_list()
    return return_json_content(content)


def get_blocked_countries(request):
    content = BlockedCountryPackageBuilder().render_all_objects_as_list()
    return return_json_content(content)


def get_blocked_ips(request):
    content = BlockedIPPackageBuilderMinimized().render_all_objects_as_list()
    return return_json_content(content)