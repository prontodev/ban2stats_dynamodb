from attack.models import Attack
from stats.models import BlockedIP


def dump_all():
    Attack.dump('attack.json')
    print 'Exported attacks to attack.json'

    BlockedIP.dump('stats.json')
    print 'Exported stats to stats.json'