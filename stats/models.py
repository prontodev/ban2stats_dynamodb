from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import LocalSecondaryIndex, AllProjection, GlobalSecondaryIndex
from django.conf import settings
from django.utils.timezone import get_current_timezone
import json
from datetime import datetime


class BlockedIP(Model):

    lat_lon = UnicodeAttribute(hash_key=True)
    attack_details = UnicodeAttribute(default="[]")
    # ip_list = UnicodeAttribute(range_key=True)
    # service_name = UnicodeAttribute()
    # protocol = UnicodeAttribute()
    # port = UnicodeAttribute()
    #
    # count = NumberAttribute(default=0)
    # last_seen = UnicodeAttribute()

    country = UnicodeAttribute()
    geo_location = UnicodeAttribute()

    class Meta:
        read_capacity_units = settings.DYNAMO_MODEL_READ_CAPACITY_UNITS
        write_capacity_units = settings.DYNAMO_MODEL_WRITE_CAPACITY_UNITS
        table_name = settings.STATS_BLOCKED_IP_TABLE_NAME
        region = settings.DYNAMODB_REGION
        host = settings.DYNAMODB_HOST


class AttackedService(Model):
    service_name = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(default=0)

    class Meta:
        read_capacity_units = settings.DYNAMO_MODEL_READ_CAPACITY_UNITS
        write_capacity_units = settings.DYNAMO_MODEL_WRITE_CAPACITY_UNITS
        table_name = settings.STATS_ATTACKED_SERVICE_TABLE_NAME
        region = settings.DYNAMODB_REGION
        host = settings.DYNAMODB_HOST


class CountIndex(LocalSecondaryIndex):

    class Meta:
        projection = AllProjection()
        index_name = "count_index"
        region = settings.DYNAMODB_REGION
        host = settings.DYNAMODB_HOST

    country_code = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(range_key=True)


class BlockedCountry(Model):
    country_code = UnicodeAttribute(hash_key=True)

    country_name = UnicodeAttribute()
    count_index = CountIndex()
    count = NumberAttribute(default=0, range_key=True)

    class Meta:
        read_capacity_units = settings.DYNAMO_MODEL_READ_CAPACITY_UNITS
        write_capacity_units = settings.DYNAMO_MODEL_WRITE_CAPACITY_UNITS
        table_name = settings.STATS_BLOCKED_COUNTRY_TABLE_NAME
        region = settings.DYNAMODB_REGION
        host = settings.DYNAMODB_HOST
