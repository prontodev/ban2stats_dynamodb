from attack.models import Attack
from stats.models import BlockedIP


def load_all():
    Attack.load('ban2stats/sample_data/attack.json')
    print 'Loaded attacks'

    BlockedIP.load('ban2stats/sample_data/stats.json')
    print 'Loaded stats'