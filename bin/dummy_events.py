#!/usr/bin/python

import base
import random
from fetch_data import models


def main():
    post = models.Morcha.objects.first()
    morchas = models.Morcha.objects.filter(post_id='7de0c922-17c7-4188-8a77-4e3bb3a5e3c0')
    print morchas.count()
    source_addr = 145555555
    dest_addr = 14555555
    payload = {'data': 'abc'}
    morchas_list = []
    for morcha in morchas:
        uuid = morcha.uuid
        morchas_list.append(uuid)
    l = len(morchas_list)
    for i in range(0, 10):
        morcha_index = random.randint(0, l-1)
        uuid = morchas_list[morcha_index]
        event = models.Event()
        event.uuid = uuid
        event.dest_addr = dest_addr
        event.source_addr = source_addr
        event.payload = payload
        rand = random.randint(0, 100)
        if rand > 90:
            event.packet_type = 4
        elif 75 < rand < 90:
            event.packet_type = 3
        else:
            event.packet_type = 2
        event.save()


if __name__ == '__main__':
    main()
