from attack.record import AttackRecorder
from attack.tests.test_models import AttackForTesting
from django.test import SimpleTestCase


class FakeAttackRecorder(AttackRecorder):

    def __init__(self, model=AttackForTesting):
        super(FakeAttackRecorder, self).__init__(model=model)


class TestAttackRecord(SimpleTestCase):

    def tearDown(self):
        AttackForTesting.delete_table()

    def test_init(self):
        attack_recorder = FakeAttackRecorder()

    def test_get_new_attack(self):

        attack = FakeAttackRecorder().new_attack()
        self.assertRaisesMessage(ValueError, "Attribute 'attacker_ip' cannot be None", attack.save)

    def test_get_geo_data(self):
        ip = '72.14.207.99'
        attack_recorder = FakeAttackRecorder()
        attack = attack_recorder.new_attack()
        geo_details = attack_recorder.get_geo_data(ip=ip)
        self.assertEqual(attack_recorder.attack.country, u'US')
        self.assertEqual(attack_recorder.attack.geo_location, u'CA, United States')

    def test_record_timestamp(self):
        attack_recorder = FakeAttackRecorder()
        attack = attack_recorder.new_attack()
        attack_recorder.record_timestamp()
        self.assertTrue(attack_recorder.attack.timestmap)

    def test_record_save(self):
        attack_recorder = FakeAttackRecorder()
        attack = attack_recorder.new_attack()
        attack_recorder.set_data(attacker_ip='72.14.207.99',
                        service_name='company web server',
                        protocol='http',
                        port='80',)
        geo_details = attack_recorder.get_geo_data()
        attack_recorder.record_timestamp()