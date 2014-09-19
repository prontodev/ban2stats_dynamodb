from attack.record import AttackRecorder
from attack.tests.test_models import AttackForTesting
from django.test import SimpleTestCase


class FakeAttackRecorder(AttackRecorder):

    def __init__(self, model=AttackForTesting):
        super(FakeAttackRecorder, self).__init__(model=model)


class TestAttackRecord(SimpleTestCase):

    def test_init(self):
        attack_recorder = FakeAttackRecorder()
        AttackForTesting.delete_table()

    def test_get_new_attack(self):

        attack = FakeAttackRecorder().new_attack()
        self.assertRaisesMessage(ValueError, "Attribute 'attacker_ip' cannot be None", attack.save)