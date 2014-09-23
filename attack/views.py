from django.http.response import HttpResponse
from attack.recorder import AttackRecorder


def add_attack(request):
    recorder = AttackRecorder()
    recorder.set_data(**request.REQUEST.copy())
    recorder.get_geo_data()
    recorder.record_timestamp()
    recorder.save()
    return HttpResponse('Added attack')