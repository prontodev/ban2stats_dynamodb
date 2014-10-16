from attack.models import Attack
from stats.models import BlockedIP


Attack.load('attack.json')
print 'Loaded attacks'

BlockedIP.load('stats.json')
print 'Loaded stats'