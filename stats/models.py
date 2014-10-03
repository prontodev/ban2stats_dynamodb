from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class BlockedIP(Model):

    category = UnicodeAttribute(range_key=True)

    key = UnicodeAttribute(hash_key=True) #IP
    service_name = UnicodeAttribute()
    protocol = UnicodeAttribute()
    port = UnicodeAttribute()
    count = NumberAttribute()
    last_seen = UnicodeAttribute()

    longitude = UnicodeAttribute()
    latitude = UnicodeAttribute()
    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'


class AttackedProtocol(Model):
    category = UnicodeAttribute(range_key=True, default='Attacked Protocol')
    key = UnicodeAttribute(hash_key=True) #Protocol

    count = NumberAttribute()

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'


class BlockedCountry(Model):
    category = UnicodeAttribute(range_key=True, default='Blocked Country')
    key = UnicodeAttribute(hash_key=True) #Country code

    country_name = UnicodeAttribute()
    count = NumberAttribute()

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'