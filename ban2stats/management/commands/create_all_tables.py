from django.core.management.base import BaseCommand
from ban2stats.utils.tables import create_all


class Command(BaseCommand):
    help = 'Create all tables.'

    def handle(self, *args, **options):
        create_all()
        self.stdout.write('Created.')