from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class Attack(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Attack'
        region = 'ap-southeast-1'
        # host = 'http://localhost:4567'

    attacker_ip = UnicodeAttribute(hash_key=True)

    service_name = UnicodeAttribute()
    protocol = UnicodeAttribute()
    port = UnicodeAttribute()

    # count = NumberAttribute(default=0)
    longitude = UnicodeAttribute()
    latitude = UnicodeAttribute()
    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()
    timestamp = UTCDateTimeAttribute(range_key=True)

