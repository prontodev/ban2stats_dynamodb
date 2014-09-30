from django.http.response import HttpResponse, HttpResponseBadRequest
from attack.recorder import AttackRecorder
from ban2stats.views import token_required

@token_required
def add_attack(request):
    print 'request.REQUEST ', request.REQUEST
    recorder = AttackRecorder()
    try:
        recorder.set_data(**request.REQUEST.copy())
    except ValueError, err:
        print err
        return HttpResponseBadRequest(err)
    try:
        recorder.get_geo_data()
    except ValueError, err:
        print err
        return HttpResponseBadRequest(err)
    recorder.record_timestamp()
    attack = recorder.save()
    print 'Added attack {0} {1} {2} {3}'.format(attack.service_name, attack.protocol, attack.port, attack.attacker_ip)
    return HttpResponse('Added attack {0} {1} {2} {3}'.format(attack.service_name, attack.protocol, attack.port, attack.attacker_ip))