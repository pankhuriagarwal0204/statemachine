import logging
import pytz
import base
import datetime


class Analyzer:
    def __init__(self, packettypes, con_redis):
        self.con_redis = con_redis
        self.packet_types = packettypes
        logging.basicConfig(filemode='w', level=logging.INFO,
                            format="%(asctime)s %(process)d %(levelname)s "
                                   "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")

    def _convert_epoch(self, dt):
        return int(dt.strftime('%s'))

    def timdiff(self, dt):
        timenow = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        timediff = timenow - dt
        return timediff.total_seconds()

    def start(self, packet_type, dt, uuid):
        uuid = str(uuid)
        if packet_type == 2:
            logging.info('start --> detected')
            obj = {
                'state': 0,
                'attempts': 1,
                'start': self._convert_epoch(dt=dt)
            }
            self.con_redis.hmset(uuid, obj)
            return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
        elif packet_type == 3:
            logging.info('start --> verified')
            start = self._convert_epoch(dt=dt)
            obj = {
                'state': 1,
                'attempts': 1,
                'start': start
            }
            self.con_redis.hmset(uuid, obj)
            return {'insert': True, 'start_time': start, 'end_time': False, 'delete': False}
        else:
            return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}

    def insert(self, packet_type, dt, uuid):
        uuid = str(uuid)
        if packet_type in self.packet_types:
            uuidstate = self.con_redis.hgetall(uuid)
            if not uuidstate:
                res = self.start(packet_type, dt, uuid)
                return res
            else:
                state = int(uuidstate['state'])
                attempts = int(uuidstate['attempts'])
                start = int(uuidstate['start'])
                if state == 0:
                    if packet_type == 2:
                        logging.info('detected --> detected')
                        obj = {
                            'state': state,
                            'attempts': attempts + 1,
                            'start': start
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    elif packet_type == 3 or packet_type == 4:
                        logging.info('detected --> verified')
                        obj = {
                            'state': 1,
                            'attempts': attempts,
                            'start': start
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': True, 'start_time': start, 'end_time': False, 'delete': False}
                    elif packet_type == 200:
                        logging.info('detected --> non human')
                        # self.con_redis.del(uuid)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': True}
                    else:
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}

                elif state == 1:
                    if packet_type == 2:
                        logging.info('verified --> attempts++')
                        obj = {
                            'attempts': attempts + 1,
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    elif packet_type == 200:
                        end = self._convert_epoch(dt=dt)
                        logging.info('verified --> marked safe')
                        obj = {
                            'state': 2,
                            'end': end
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    elif packet_type == 702:
                        logging.info('verified --> ignored')
                        obj = {
                            'state': 3
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    else:
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}

                elif state == 2:
                    if packet_type == 2:
                        logging.info('marked safe --> detected')
                        obj = {
                            'attempts': attempts + 1
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    elif packet_type == 3:
                        logging.info('marked safe --> verified')
                        obj = {
                            'state': 3,
                            'attempts': attempts + 1
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}


                elif state == 3:
                    if packet_type == 200:
                        end = self._convert_epoch(dt=dt)
                        logging.info('sos --> markedsafe')
                        obj = {
                            'state': 2,
                            'end': end
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': False, 'start_time': False, 'end_time': False, 'delete': False}
                    if packet_type == 701:
                        end = self._convert_epoch(dt=dt)
                        logging.info('sos --> neutralized')
                        obj = {
                            'state': 5,
                            'end': end
                        }
                        self.con_redis.hmset(uuid, obj)
                        return {'insert': True, 'start_time': False, 'end_time': end, 'delete': False}

                elif state == 4:
                    pass

                elif state == 5:
                    res = self.start(packet_type=packet_type, dt=dt, uuid=uuid)
                    return res


                elif state == 6:
                    res = self.start(packet_type=packet_type, dt=dt, uuid=uuid)
                    return res

        else:
            return {'new': False, 'insert': False}