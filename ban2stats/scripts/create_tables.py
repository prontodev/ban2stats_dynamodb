from attack.models import Attack
from stats.models import BlockedIP


def create_all():
    if not Attack.exists():
        Attack.create_table(wait=True)

    if not BlockedIP.exists():
        BlockedIP.create_table(wait=True)