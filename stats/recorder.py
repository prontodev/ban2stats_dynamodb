from stats.models import BlockedIP
from django.utils.timezone import get_current_timezone
from datetime import datetime


class StatsRecorder(object):

    def __init__(self, data):
        self.data = data
        self.ip = self.data['attacker_ip']

        if not BlockedIP.exists():
            BlockedIP.create_table(wait=True)

    def get_blocked_ip_category(self):
        category = 'blocked_ip_{0}'.format(self.ip)
        return category

    def get_existing_banned_ip_record(self):
        existing_blocked_ip = BlockedIP.query(self.ip, category=self.get_blocked_ip_category(),
                                               service_name=self.data['service_name'], Count=True)
        existing_records = []
        for item in existing_blocked_ip:
            print 'service_name = ', item.service_name
            print 'count = ', item.count
            existing_records.append(item)
        print '-----'
        return existing_records

    def get_existing_banned_ip_count(self):
        try:
            existing_record = self.get_existing_banned_ip_record()[0]
        except IndexError, err:
            return 1
        count = existing_record.count + 1
        return count

    def save_banned_ip_record(self):
        category = self.get_blocked_ip_category()
        count = self.get_existing_banned_ip_count()
        last_seen = unicode(datetime.now(tz=get_current_timezone()))
        self.blocked_ip = BlockedIP(
            category=category,
            key=self.ip,
            service_name=self.data['service_name'],
            protocol=self.data['protocol'],
            port=self.data['port'],
            longitude=self.data['longitude'],
            latitude=self.data['latitude'],
            country=self.data['country'],
            geo_location=self.data['geo_location'],
            count=count,
            last_seen=last_seen,
        )
        self.blocked_ip.save()
        return self.blocked_ip

    def delete_table(self):
        BlockedIP.delete_table()
