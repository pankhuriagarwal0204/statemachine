#!/usr/bin/python
import time

import base
from fetch_data import models
import logging
import redis
from analyzer import Analyzer

packettypes_to_copy = [1, 2, 3, 4, 200, 500, 601, 603]
packettypes_to_shrink = (2, 3, 4, 200)
LAST_PROCESSED = "last_processed"
con_redis = redis.Redis(host='localhost', db=2)


def insert_event(row):
    if row.packet_type == 601 or row.packet_type == 603:
        batterylog = models.Batterylog()
        batterylog.battery_level = int(row.payload['battery_level'])
        batterylog.charging = row.payload['charging']
        batterylog.detected_datetime = row.req_datetime
        try:
            morcha = models.Morcha.objects.get(uuid=row.uuid)
            batterylog.morcha = morcha
            batterylog.save()

        except Exception as e:
            print e
            try:
                device = models.Device.objects.get(uuid=row.uuid)
                batterylog.device = device
                batterylog.morcha = device.morcha
                batterylog.save()
            except Exception as e:
                print e

    else:
        res = analyzerObj.insert(row.packet_type, row.req_datetime, row.uuid)
        if not res['insert']:
            logging.info("Skipping the event id: %d, time: %s, uuid: %s", row.id, row.req_datetime, row.uuid)
            return
        else:
            logging.info("Inserting the intrusion id: %d, time: %s, uuid: %s", row.id, row.req_datetime, row.uuid)
            try:
                morcha_obj = models.Morcha.objects.get(uuid=row.uuid)
            except Exception as e:
                logging.info("Error while getting morcha of uuid: %s, time: %s for intrusion id: %d - %s",
                             row.uuid, row.req_datetime, row.id, e)
                return
            if res['new']:
                intrusion_obj = models.Intrusion()
                intrusion_obj.detected_datetime = row.req_datetime
                intrusion_obj.morcha = morcha_obj
                intrusion_obj.save()
            if row.packet_type == 2:
                pass
            elif row.packet_type == 3:
                intrusion_obj = models.Intrusion.objects.filter(morcha=morcha_obj, verified_datetime__isnull=True). \
                    order_by('-detected_datetime').first()
                intrusion_obj.verified_datetime = row.req_datetime
                intrusion_obj.save()
            elif row.packet_type == 200:
                if res['non_human']:
                    intrusion_obj = models.Intrusion.objects.filter(morcha=morcha_obj,
                                                                    neutralized_datetime__isnull=True,
                                                                    verified_datetime__isnull=True). \
                        order_by('-detected_datetime').first()
                    intrusion_obj.non_human_intrusion_datetime = row.req_datetime
                    intrusion_obj.save()
                else:
                    intrusion_obj = models.Intrusion.objects.filter(morcha=morcha_obj, verified_datetime__isnull=False,
                                                                    neutralized_datetime__isnull=True). \
                        order_by('-detected_datetime').first()
                    intrusion_obj.neutralized_datetime = row.req_datetime
                    intrusion_obj.save()
            else:
                pass


def analyzer(last_processed=None):
    logging.info("Selecting events table for the id '%r' and packet types '%s'", last_processed, packettypes_to_copy)

    if last_processed is not None:
        last_processed = int(last_processed)
        rows = models.Event.objects.filter(packet_type__in=packettypes_to_copy, id__gt=last_processed). \
            order_by('id')
    else:
        rows = models.Event.objects.filter(packet_type__in=packettypes_to_copy).order_by('id')

    logging.info("Events query : %s", rows.query)

    for row in rows:
        insert_event(row)
        con_redis.set(LAST_PROCESSED, row.id)

    logging.info("Processed record count : %d", rows.count())
    print rows.count()


def get_last_processed_record():
    a = con_redis.get(LAST_PROCESSED)
    return a


def main():
    last_processed = get_last_processed_record()
    analyzer(last_processed)


if __name__ == '__main__':
    logging.basicConfig(filename='process.log', level=logging.INFO,
                        format="%(asctime)s %(process)d %(levelname)s "
                               "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")
    analyzerObj = Analyzer(packettypes_to_shrink, con_redis)
    while True:
        main()
        time.sleep(3)
