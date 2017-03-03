#!/usr/bin/python

import base
from fetch_data import models
import logging
import time
import sys
from uuid import UUID


def main(key=None):
    morchas = models.Morcha.objects.all()
    source_addr = 145555555
    dest_addr = 14555555
    payload = {'data': 'abc'}
    for morcha in morchas:
        uuid = morcha.uuid
        if key == 'random':
            for i in range(0, 200):
                if i%3 == 0:
                    print i
                    event = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                          payload=payload)
                    event.save()
                elif i%5 == 0:
                    print i
                    event = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                          payload=payload)
                    event.save()
                elif i%11 == 0:
                    print i
                    event = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                          payload=payload)
                    event.save()
                else:
                    print i
                    event = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                          payload=payload)
                    event.save()
                # time.sleep(1)

        elif key == 'dsn':
            eventd = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventd.save()
            events = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            events.save()
            eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventn.save()

        elif key == 'dn':
            eventd = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventd.save()
            eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventn.save()

        elif key == 's':
            uuid = 'a4914525-7c81-4586-a4bf-a88280641a4d'
            for i in range(0, 1):
                events = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                events.save()

        elif key == 'd':
            eventd = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventd.save()


        elif key == 'n':
            for i in range(0, 10):
                eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                eventn.save()

        elif key == 'nsn':
            eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                     payload=payload)
            eventn.save()
            events = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            events.save()
            eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                  payload=payload)
            eventn.save()

        elif key == 'bl':
            uuid_ = UUID('921ff28d071d4c6e8b3e176721da119f')
            payload = {'battery_level': '65', 'charging': 'True'}
            event = models.Event(packet_type=601, dest_addr=dest_addr, source_addr=source_addr, uuid=uuid_,
                                 payload=payload)
            event.save()
            break

        else:
            print "in else part"
            for i in range(0, 10):
                eventn = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                eventn.save()
                eventd = models.Event(uuid=uuid, packet_type=2, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                eventd.save()
                events = models.Event(uuid=uuid, packet_type=3, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                events.save()
                eventn = models.Event(uuid=uuid, packet_type=4, dest_addr=dest_addr, source_addr=source_addr,
                                      payload=payload)
                eventn.save()


if __name__ == '__main__':
    logging.basicConfig(filemode='w', level=logging.INFO,
                        format="%(asctime)s %(process)d %(levelname)s "
                               "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")
    key = sys.argv[1:][0]
    main(key)
