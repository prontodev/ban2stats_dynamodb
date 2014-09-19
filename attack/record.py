from attack.models import Attack


class AttackRecord(object):

    def __init__(self, model=Attack):
        self.model = model
        if not self.model.exists():
            self.model.create_table(wait=True)

    def new_attack(self):
        self.attack = self.model()
        return self.attack
