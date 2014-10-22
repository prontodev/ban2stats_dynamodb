from django.core.management.base import BaseCommand
from ban2stats.utils.tables import delete_all


class Command(BaseCommand):
    help = 'Delete all tables.'

    def handle(self, *args, **options):
        delete_all()
        self.stdout.write('Deleted.')