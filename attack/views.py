from django.http.response import HttpResponse


def add_attack(request):

    # attack.save()
    return HttpResponse('Added attack')