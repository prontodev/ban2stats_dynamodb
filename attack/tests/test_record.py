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

    def test_get_geo_data(self):
        ip = '72.14.207.99'
        attack_recorder = FakeAttackRecorder()
        attack = attack_recorder.new_attack()
        geo_details = attack_recorder.get_geo_data(ip=ip)
        self.assertEqual(attack_recorder.attack.country, u'United States')
        self.assertEqual(attack_recorder.attack.geo_location, '')