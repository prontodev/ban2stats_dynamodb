from django.http.response import HttpResponse


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
    var data = {};
    """
    return HttpResponse(content)
