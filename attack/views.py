from django.http.response import HttpResponse


def add_attack(request):
    return HttpResponse('Add attack')