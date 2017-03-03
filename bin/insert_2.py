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
    morcha_list = []
    for morcha in morchas:
        uuid = morcha.uuid
        morcha_list.append(uuid)

    if key == 'un4':
        event = models.Event(uuid=morcha_list[0], packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[1], packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[1], packet_type=3, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[0], packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[0], packet_type=3, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[0], packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=morcha_list[0], packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        # event = models.Event(uuid=morcha_list[1], packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()
        # event = models.Event(uuid=morcha_list[1], packet_type=703, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()
        # event = models.Event(uuid=morcha_list[0], packet_type=703, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()

    if key == 'd3':
        uuid = 'ad93ddf2-4c16-4ebd-b67f-4bfd138917a0'
        event = models.Event(uuid=uuid, packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=3, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=703, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        # event = models.Event(uuid=uuid, packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()
        # event = models.Event(uuid=uuid, packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()
        # event = models.Event(uuid=uuid, packet_type=2, source_addr=source_addr, dest_addr=dest_addr,
        #                      payload=payload)
        # event.save()

    if key == 'un1':
        uuid = 'ad93ddf2-4c16-4ebd-b67f-4bfd138917a0'
        event = models.Event(uuid=uuid, packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=3, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=701, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=200, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()
        event = models.Event(uuid=uuid, packet_type=703, source_addr=source_addr, dest_addr=dest_addr,
                             payload=payload)
        event.save()


if __name__ == '__main__':
    logging.basicConfig(filemode='w', level=logging.INFO,
                        format="%(asctime)s %(process)d %(levelname)s "
                               "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")
    key = sys.argv[1:][0]
    main(key)
