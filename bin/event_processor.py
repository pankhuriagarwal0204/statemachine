import pytz
import redis
import datetime
import base
from fetch_data import models as fetch_data_models
import machine


MORCHA_LIST = 'morcha_uuid'
LAST_PROCESSED = 'last_processed'
con_redis = redis.Redis(host='localhost', db=1)

class EventProcessor:
    def __init__(self):
        self.morcha_machines = {}
        morchas = list(con_redis.smembers(MORCHA_LIST))
        for morcha in morchas:
            self.state_key = "state:" + morcha
            data = con_redis.hgetall(self.state_key)
            if data:
                end_time = EventProcessor._convert_string_to_datetime(data['end_time'])
                start_time = EventProcessor._convert_string_to_datetime(data['start_time'])
                attempts = int(data['attempts'])
                self.morcha_machines[str(morcha)] = machine.MorchaStateMachine(uuid=morcha, current_state=data['state'],
                                                                               intrusion_attempts=attempts,
                                                                               latest_intrusion_end_time=end_time,
                                                                               latest_intrusion_start_time=start_time)
            else:
                self.morcha_machines[str(morcha)] = machine.MorchaStateMachine(uuid=morcha)

    @staticmethod
    def _convert_string_to_datetime(str):
        if len(str) > 25:
            str = str[:25]
            c = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S.%f')
            c = c.replace(tzinfo=pytz.UTC)
            return c
        else:
            return None

    def processor(self, row):
        morcha_uuid = row.uuid
        morcha_machine = self.morcha_machines[str(morcha_uuid)]
        if row.packet_type == 2:
            morcha_machine.intrusion_detected(current_time = row.req_datetime)
        elif row.packet_type == 3:
            morcha_machine.intrusion_verified_button_pressed(current_time = row.req_datetime)
        elif row.packet_type == 4:
            morcha_machine.intrusion_verified_button_pressed(current_time = row.req_datetime)
        elif row.packet_type == 200:
            morcha_machine.area_secure_button_pressed(current_time = row.req_datetime)
        elif row.packet_type == 701:
            morcha_machine.sos_raised_button_pressed(current_time = row.req_datetime)
        elif row.packet_type == 703:
            morcha_machine.security_confirmed_event(current_time = row.req_datetime)
        else:
            print "invalid packet type"
        morcha_machine.save_instance(redis=con_redis)
        con_redis.set(LAST_PROCESSED, row.id)


def get_last_processed():
    a = con_redis.get(LAST_PROCESSED)
    return a


def main():
    val = get_last_processed()
    if val is not None:
        val = int(val)
        events = fetch_data_models.Event.objects.filter(id__gt=val).order_by('id')
    else:
        events = fetch_data_models.Event.objects.all().order_by('id')

    for row in events:
        event_processor.processor(row=row)


if __name__ == '__main__':
    event_processor = EventProcessor()
    main()



