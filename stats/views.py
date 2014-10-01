from django.http.response import HttpResponse


def get_stats(request):
    return HttpResponse("var data = {}")
