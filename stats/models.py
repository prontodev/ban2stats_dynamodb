from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class BlockedIP(Model):

    category = UnicodeAttribute(range_key=True)

    key = UnicodeAttribute(hash_key=True) #IP
    service_name = UnicodeAttribute()
    protocol = UnicodeAttribute()
    port = UnicodeAttribute()
    count = NumberAttribute(default=0)
    last_seen = UnicodeAttribute()

    longitude = NumberAttribute()
    latitude = NumberAttribute()
    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'
        host = 'http://localhost:4567'


class AttackedService(Model):
    category = UnicodeAttribute(range_key=True, default='attacked_service')
    key = UnicodeAttribute(hash_key=True) #Protocol

    count = NumberAttribute(default=0)

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'
        host = 'http://localhost:4567'


class BlockedCountry(Model):
    category = UnicodeAttribute(range_key=True, default='blocked_country')
    key = UnicodeAttribute(hash_key=True) #Country code

    country_name = UnicodeAttribute()
    count = NumberAttribute(default=0)

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'
        host = 'http://localhost:4567'