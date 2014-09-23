from django.http.response import HttpResponse


def add_attack(request):
    print 'ddd'
    # attack.save()
    return HttpResponse('Added attack')