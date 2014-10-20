from django.http.response import HttpResponse
from stats.packages.attacked_service import AttackedServicePackageBuilder
from stats.packages.blocked_ip import BlockedIPPackageBuilder
from stats.packages.blocked_country import BlockedCountryPackageBuilder


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
