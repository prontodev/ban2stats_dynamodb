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
    var pins = [
        { blocked_ip: "72.14.207.99", service_name: "Internal Wordpress System", protocol: "http", port: "80",
          count: "30", last_seen: "Sep 27, 2014 12:33",
          latitude: 37.419200897216797, longitude: "-122.05740356445312",
          geo_location: "CA, United States"
        }
    ];
    var attacked_services = [
                ['Internal Wordpress System', 32,923],
                ['Mail Server', 923],
                ['Company Secured Server', 127,563],
    ];
    """
    return HttpResponse(content)
