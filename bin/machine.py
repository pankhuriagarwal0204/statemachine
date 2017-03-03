from transitions import Machine
from machine_transitions import *
import base
from fsm import models as fsm_models
from fetch_data import models as fetch_data_models


class UnitStateMachine(object):
    def __init__(self, uuid, morcha):
        self.states = ['sleeping', 'ringing']
        self.morcha = morcha
        self.uuid = uuid
        self.machine = Machine(self, states=self.states, initial='start')
        self.machine.add_transition('ID', 'start', 'ringing', after='after_intrusion_detected')
        self.machine.add_transition('intrusion_never_happened', 'ringing', 'start')

    def after_intrusion_detected(self):
        self.morcha.intrusion_detected()


class MorchaStateMachine(object):
    def __init__(self, uuid, post=None, current_state='secure', intrusion_attempts=0, latest_intrusion_start_time=None,
                 latest_intrusion_end_time=None):
        self.uuid = uuid
        self.post = post
        self.start_time = latest_intrusion_start_time
        self.end_time = latest_intrusion_end_time
        self.machine = Machine(model=self, states=morcha_states, transitions=morcha_transitions, initial=current_state)
        self.intrusion_attempts = intrusion_attempts

    def after_intrusion_detected(self, current_time=None):
        self.start_time = current_time

    def increase_attempts(self, current_time=None):
        self.intrusion_attempts += 1
        morcha_intrusion = fsm_models.newIntrusion.objects.filter(morcha=self.uuid, end_time__isnull=True).order_by(
            '-start_time').first()
        morcha_intrusion.attempts = self.intrusion_attempts
        morcha_intrusion.save()

    def intrusion_never_happened(self, current_time=None):
        self.intrusion_attempts = 0
        self.start_time = None
        self.end_time = None

    def after_intrusion_verified(self, current_time=None):
        intrusion = fsm_models.newIntrusion()
        morcha = fetch_data_models.Morcha.objects.get(uuid=self.uuid)
        intrusion.morcha = morcha
        intrusion.start_time = self.start_time
        intrusion.attempts = self.intrusion_attempts
        intrusion.save()

    def after_marked_safe(self, current_time=None):
        self.end_time = current_time

    def after_sos_raised(self, current_time=None):
        pass

    def marked_safe_to_verified(self, current_time=None):
        pass

    def after_security_confirmed(self, current_time=None):
        morcha_intrusion = fsm_models.newIntrusion.objects.filter(morcha=self.uuid, end_time__isnull=True).order_by(
            '-start_time').first()
        morcha_intrusion.end_time = self.end_time
        morcha_intrusion.save()

    def save_instance(self, redis=None):
        key = "state:" + str(self.uuid)
        obj = {
            'state': self.state,
            'attempts': self.intrusion_attempts,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        redis.hmset(key, obj)


class PostStateMachine(object):
    def __init__(self):
        self.states = ['intrusion detected', 'unit down', 'marked safe', 'intrusion verified', 'end']
        self.machine = Machine(self, states=self.states, initial='start')

# post1 = PostStateMachine()
# morcha1 = MorchaStateMachine(post1)
# unit1 = UnitStateMachine(morcha1)
#
# # To be extracted from django
# unit_qs = {}
# morcha_qs = {}
# post_qs = {}
#
# unit_dict = {}
# morcha_dict = {}
# post_dict = {}

# def create_post_machine(_uuid):
#     return PostStateMachine()
#
#
# def create_morcha_machine(_uuid):
#     post = post_dict[morcha_qs['morcha_uuid']['post_id']] or create_morcha_machine('morcha_uuid')
#
#
# for i in unit_qs:
#     morcha = morcha_dict['morcha_uuid'] or create_morcha_machine('morcha_uuid')
#     unit_dict = {i: UnitStateMachine(morcha)}
# morchas = {}
# for i in morchas:
#     MorchaStateMachine()
#
# truth = []
# for i in truth:
#     event = truth['event']  # this is a string
#     entity_type = truth['entity_type']
#     if entity_type == 'morcha':
#         getattr(morcha_dict[i['morcha']], event)
#
# for i in morcha:
#     redis.set(morcha, morcha_dict['morcha_id'])
