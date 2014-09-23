from django.http.response import HttpResponse, HttpResponseBadRequest
from attack.recorder import AttackRecorder


def add_attack(request):
    recorder = AttackRecorder()
    try:
        recorder.set_data(**request.REQUEST.copy())
    except ValueError, err:
        return HttpResponseBadRequest(err)
    recorder.get_geo_data()
    recorder.record_timestamp()
    recorder.save()
    return HttpResponse('Added attack')