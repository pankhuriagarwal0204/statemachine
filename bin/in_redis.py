#!/usr/bin/python
"""
The initialisation of the data needed by the apis
currently has morcha data which is the place where intrusion happens
"""
import base
import redis
import time
from fetch_data import models

# redis config
# db 1 denotes persistent cache
config = {'host': 'localhost', 'db': 1}
conn = redis.Redis(**config)


def fetch_now_utc():
    return time.time()*1000


def insert_in_postgres():
    geospace_1 = models.Geospace(latitude=32.45777715387119, longitude=75.12176513671876)
    geospace_1.save()
    geospace_2 = models.Geospace(latitude=32.476315491147616, longitude=75.11077880859376)
    geospace_2.save()
    geospace_3 = models.Geospace(latitude=32.48239755141864, longitude=75.09223937988283)
    geospace_3.save()
    geospace_4 = models.Geospace(latitude=32.48963756347198, longitude=75.07593154907228)
    geospace_4.save()
    geospace_5 = models.Geospace(latitude=32.49398129108325, longitude=75.05395889282228)
    geospace_5.save()
    geospace_6 = models.Geospace(latitude=32.49164656356051, longitude=75.12032043188812)
    geospace_6.save()

    battalion_1 = models.Battalion(name='battalion1', geospace=geospace_1)
    battalion_1.save()

    post_1 = models.Post(name='post1', geospace=geospace_6, battalion=battalion_1)
    post_1.save()

    morcha_1 = models.Morcha(name='Morcha-111', geospace=geospace_1, post=post_1)
    morcha_1.save()
    morcha_2 = models.Morcha(name='Morcha-242', geospace=geospace_2, post=post_1)
    morcha_2.save()
    morcha_3 = models.Morcha(name='Morcha-345', geospace=geospace_3, post=post_1)
    morcha_3.save()
    morcha_4 = models.Morcha(name='Morcha-563', geospace=geospace_4, post=post_1)
    morcha_4.save()
    morcha_5 = models.Morcha(name='Morcha-123', geospace=geospace_5, post=post_1)
    morcha_5.save()

    device_1 = models.Device(repr = 'qrt1', morcha=morcha_1)
    device_1.save()
    device_1 = models.Device(repr='tx1', morcha=morcha_1)
    device_1.save()
    device_1 = models.Device(repr='rx1', morcha=morcha_1)
    device_1.save()
    device_2 = models.Device(repr='qrt2', morcha=morcha_2)
    device_2.save()
    device_2 = models.Device(repr='tx2', morcha=morcha_2)
    device_2.save()
    device_2 = models.Device(repr='rx2', morcha=morcha_2)
    device_2.save()
    device_3 = models.Device(repr='qrt3', morcha=morcha_3)
    device_3.save()
    device_3 = models.Device(repr='tx3', morcha=morcha_3)
    device_3.save()
    device_3 = models.Device(repr='rx3', morcha=morcha_3)
    device_3.save()
    device_4 = models.Device(repr='qrt4', morcha=morcha_4)
    device_4.save()
    device_4 = models.Device(repr='tx4', morcha=morcha_4)
    device_4.save()
    device_4 = models.Device(repr='rx4', morcha=morcha_4)
    device_4.save()
    device_5 = models.Device(repr='qrt5', morcha=morcha_5)
    device_5.save()
    device_5 = models.Device(repr='tx5', morcha=morcha_5)
    device_5.save()
    device_5 = models.Device(repr='rx5', morcha=morcha_5)
    device_5.save()


def delete_in_postgres():
    models.Geospace.objects.all().delete()


def insert_in_redis():
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid,
            "qrt": True
        }
        devices = morcha.devices.all()
        for device in devices:
            obj[device.device_type] = True
        conn.hmset(morcha.uuid, obj)
        conn.sadd("morcha_uuid", morcha.uuid)


if __name__ == '__main__':
    # insert_in_postgres()
    #delete_in_postgres()
    insert_in_redis()
