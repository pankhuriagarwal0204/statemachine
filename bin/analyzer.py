import logging
import pytz
import base
import datetime


class Analyzer:
    def __init__(self, packettypes, con_redis):
        self.con_redis = con_redis
        self.packet_types = packettypes
        self.state_to_packet = {
            0: 2,
            1: [3,4],
            2: 200
        }
        logging.basicConfig(filemode='w', level=logging.INFO,
                            format="%(asctime)s %(process)d %(levelname)s "
                                   "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")

    def _convert_epoch(self, dt):
        return int(dt.strftime('%s'))

    def timdiff(self, dt):
        timenow = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        timediff = timenow - dt
        return timediff.total_seconds()

    def insert(self, packet_type, dt, uuid):
        uuid = str(uuid)
        if packet_type in self.packet_types:
            # conditions to check start of sm
            uuidstate = self.con_redis.get(uuid)
            if not uuidstate:
                # if current packet is intrusion detected
                if packet_type == self.state_to_packet[0]:
                    logging.info("start --> detected")
                    self.con_redis.set(uuid, 0)
                    return {'insert': True, 'new': True, 'non_human': False}
                # if current packet is intrusion verified
                elif packet_type in self.state_to_packet[1]:
                    logging.info("start --> verified")
                    self.con_redis.set(uuid, 1)
                    return {'insert': True, 'new': True, 'non_human': False}
                else:
                    return {'insert': False, 'new': False, 'non_human': False}
            # checking for each state the possible transitions
            # checking transition for state 0: 0--1, 0--2
            elif int(uuidstate) == 0:
                if packet_type == self.state_to_packet[0]:
                    return {'insert': False, 'new': False, 'non_human': False}
                elif packet_type in self.state_to_packet[1]:
                    logging.info("detected --> verified")
                    self.con_redis.set(uuid, 1)
                    return {'insert': True, 'new': False, 'non_human': False}
                elif packet_type == self.state_to_packet[2]:
                    logging.info("detected --> non_human")
                    self.con_redis.set(uuid, 2)
                    return {'insert': True, 'new': False, 'non_human': True}
                else:
                    return {'insert': False, 'new': False, 'non_human': False}
            # checking for state 1: 1--2
            elif int(uuidstate) == 1:
                # print packet_type, type(packet_type)
                # print self.state_to_packet[2], type(self.state_to_packet[2])
                if packet_type == self.state_to_packet[0]:
                    return {'insert': False, 'new': False, 'non_human': False}
                elif packet_type in self.state_to_packet[1]:
                    return {'insert': False, 'new': False, 'non_human': False}
                elif packet_type == self.state_to_packet[2]:
                    logging.info("verified --> neutralized")
                    self.con_redis.set(uuid, 2)
                    return {'insert': True, 'new': False, 'non_human': False}
                else:
                    return {'insert': False, 'new': False, 'non_human': False}
            # checking for state 2: 2--0, 2--1
            elif int(uuidstate) == 2:
                if packet_type == self.state_to_packet[0]:
                    logging.info("neutralized/non_human --> detected")
                    self.con_redis.set(uuid, 0)
                    return {'insert': True, 'new': True, 'non_human': False}
                elif packet_type in self.state_to_packet[1]:
                    logging.info("neutralized/non_human --> verified")
                    self.con_redis.set(uuid, 1)
                    return {'insert': True, 'new': True, 'non_human': False}
                elif packet_type == self.state_to_packet[2]:
                    return {'insert': False, 'new': False, 'non_human': False}
                else:
                    return {'insert': False, 'new': False, 'non_human': False}
        else:
            return {'insert': False, 'new': False, 'non_human': False}
