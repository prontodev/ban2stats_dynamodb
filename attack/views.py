from django.http.response import HttpResponse, HttpResponseBadRequest
from attack.recorder import AttackRecorder
from stats.recorder import StatsRecorder
from ban2stats.views import token_required

@token_required
def add_attack(request):
    attack_recorder = AttackRecorder()
    try:
        attack_recorder.set_data(**request.REQUEST.copy())
    except ValueError, err:
        print err
        return HttpResponseBadRequest(err)
    try:
        attack_recorder.get_geo_data()
    except ValueError, err:
        print err
        return HttpResponseBadRequest(err)
    attack_recorder.record_timestamp()

    stats_recorder = StatsRecorder(attack_recorder.data)
    stats_recorder.save_blocked_ip_record()
    stats_recorder.save_attacked_service_record()
    stats_recorder.save_blocked_country_record()

    attack = attack_recorder.save()
    print 'Added attack {0} {1} {2} {3}'.format(attack.service_name, attack.protocol, attack.port, attack.attacker_ip)


    return HttpResponse('Added attack {0} {1} {2} {3}'.format(attack.service_name, attack.protocol, attack.port, attack.attacker_ip))