from django.http.response import HttpResponse, HttpResponseBadRequest
from attack.recorder import AttackRecorder
from ban2stats.views import token_required

@token_required
def add_attack(request):
    recorder = AttackRecorder()
    try:
        recorder.set_data(**request.REQUEST.copy())
    except ValueError, err:
        return HttpResponseBadRequest(err)
    try:
        recorder.get_geo_data()
    except ValueError, err:
        return HttpResponseBadRequest(err)
    recorder.record_timestamp()
    recorder.save()
    return HttpResponse('Added attack')