from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import LocalSecondaryIndex, AllProjection, GlobalSecondaryIndex
from django.conf import settings


class CountIndex(LocalSecondaryIndex):

    class Meta:
        projection = AllProjection()
        index_name = "count_index"
        region = 'ap-southeast-1'
        host = settings.DYNAMODB_HOST

    category = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(range_key=True)


class BlockedIP(Model):

    category = UnicodeAttribute(hash_key=True)

    key = UnicodeAttribute(range_key=True) #IP
    service_name = UnicodeAttribute()
    protocol = UnicodeAttribute()
    port = UnicodeAttribute()

    count_index = CountIndex()
    count = NumberAttribute(default=0)
    last_seen = UnicodeAttribute()

    longitude = UnicodeAttribute()
    latitude = UnicodeAttribute()
    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()

    class Meta:
        read_capacity_units = 4
        write_capacity_units = 4
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'
        host = settings.DYNAMODB_HOST


class AttackedService(Model):
    category = UnicodeAttribute(hash_key=True, default='attacked_service')
    key = UnicodeAttribute(range_key=True) #Protocol
    count_index = CountIndex()
    count = NumberAttribute(default=0)

    class Meta:
        read_capacity_units = 4
        write_capacity_units = 4
        table_name = 'Ban2Stats_Stats'
        region = 'ap-southeast-1'
        host = settings.DYNAMODB_HOST


class BlockedCountry(Model):
    category = UnicodeAttribute(hash_key=True, default='blocked_country')
    key = UnicodeAttribute(range_key=True) #Country code

    country_name = UnicodeAttribute()
    count_index = CountIndex()
    count = NumberAttribute(default=0)

    class Meta:
        read_capacity_units = 4
        write_capacity_units = 4
        table_name = 'Ban2Stats_Stats'
        region = settings.DYNAMODB_REGION
        host = settings.DYNAMODB_HOST
