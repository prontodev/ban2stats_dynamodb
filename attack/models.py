from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class Attack(Model):
    class Meta:
        table_name = 'Attack'
        host = 'http://localhost:4567'

    attacker_ip = UnicodeAttribute(range_key=True)
    attack_id = NumberAttribute(hash_key=True)

    service_name = UnicodeAttribute()
    protocol = UnicodeAttribute()
    port = UnicodeAttribute()

    # count = NumberAttribute(default=0)
    longitude = UnicodeAttribute()
    latitude = UnicodeAttribute()
    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()
    timestmap = UTCDateTimeAttribute()