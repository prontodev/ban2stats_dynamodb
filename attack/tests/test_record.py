from attack.record import AttackRecord
from attack.tests.test_models import AttackForTesting


class FakeAttackRecord(AttackRecord):

    def __init__(self, model=AttackForTesting):
        super(self, FakeAttackRecord).__init__(model=model)