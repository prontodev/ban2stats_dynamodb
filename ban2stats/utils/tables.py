from attack.models import Attack
from stats.models import BlockedIP, BlockedCountry, AttackedService


def create_all():
    if not Attack.exists():
        Attack.create_table(wait=True)

    if not BlockedIP.exists():
        BlockedIP.create_table(wait=True)

    if not BlockedCountry.exists():
        BlockedCountry.create_table(wait=True)

    if not AttackedService.exists():
        AttackedService.create_table(wait=True)


def delete_all():
    Attack.delete_table()
    BlockedIP.delete_table()
    BlockedCountry.delete_table()
    AttackedService.delete_table()