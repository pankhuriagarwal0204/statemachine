import datetime

import pytz
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
import time
import redis
import models

# use redis connection config from settings.py
conn = redis.Redis(**settings.REDIS_CONN_SETTINGS)


def fetch_now_utc():
    t = time.time()
    return t*1000


def above_last_updated_threshold(time_from_redis):
    current_time = fetch_now_utc()
    time_from_redis = float(time_from_redis/1000)
    difference = current_time - time_from_redis
    if difference > settings.UPDATE_THRESHOLD:
        return True
    else:
        return False


def above_unit_status_threshold(time_from_redis):
    current_time = fetch_now_utc()
    time_from_redis = float(time_from_redis)
    difference = current_time - time_from_redis
    if difference > settings.UNIT_STATUS_THRESHOLD:
        return True
    else:
        return False


def above_detected_sos_threshold(time_from_redis):
    current_time = fetch_now_utc()
    time_from_redis = float(time_from_redis)
    difference = current_time - time_from_redis
    print difference
    if difference > settings.SOS_DETECTED_GAP:
        return True
    else:
        return False


# list complete morcha data from redis
# list view
def fetch_morchas(request):
    _morcha_data = []
    # morcha_ids contains list of all the uuids of morcha
    morcha_ids = conn.smembers('morcha_uuid')
    morcha_ids = list(morcha_ids)

    for morcha in morcha_ids:

        # retrieve the detail of the morcha
        morcha_data = conn.hgetall(morcha)
        morcha_data.pop('unit', None)
        # if intrusion has happened on morcha
        if "intrusion" in morcha_data:
            # intrsuion_id refers to key of intrusion associated with the morcha
            intrusion_id = morcha_data['intrusion']
            intrusion_info = conn.hgetall(intrusion_id)
            if above_detected_sos_threshold(intrusion_info['detected']):
                if 'sos' not in intrusion_info and 'neutralized' not in intrusion_info:
                    # 300000 (ms) = 5 min
                    intrusion_info['sos'] = float(intrusion_info['detected']) + 300000
                    conn.hmset(intrusion_id, intrusion_info)
                    intrusion_info = conn.hgetall(intrusion_info)
            # set intrusion info to data fetched from intrusion table
            if 'sos' in intrusion_info:
                morcha_data['status'] = 'sos'
            elif 'detected' in intrusion_info:
                morcha_data['status'] = 'detected'
            else:
                morcha_data['status'] = 'neutralized'
            # remove this field --> added for legacy version
            morcha_data['intrusion'] = intrusion_info
        else:
            morcha_data['status'] = ''
            morcha_data['intrusion'] = {}
        morcha_data['active'] = True

        _morcha_data.append(morcha_data)
    return JsonResponse(_morcha_data, safe=False)


# returns details of a single morcha
# detail view
def fetch_intruded_morcha_details(request, morcha_id):
    # res = {}
    # morcha_data = conn.hgetall(morcha_id)
    # res['start_time'] = ''
    # res['end_time'] = ''
    # if 'intrusion' in morcha_data:
    #     intrusion_id = morcha_data['intrusion']
    #     intrusion_info = conn.hgetall(intrusion_id)
    #     if 'detected' in intrusion_info:
    #         val = int(intrusion_info['detected'])
    #         val = val/1000.0
    #         res['start_time']= datetime.datetime.fromtimestamp(val)
    #
    #     if 'neutralized' in intrusion_info:
    #         val = int(intrusion_info['neutralized'])
    #         val = val/1000.0
    #         res['end_time'] = datetime.datetime.fromtimestamp(val)
    #
    # unit_inactive = above_unit_status_threshold(morcha_data['last_updated'])
    # print "unit active for %r is" % morcha_data['uuid'], not unit_inactive
    # if unit_inactive:
    #     res['qrt'] = False
    #     res['unit'] = False
    # else:
    #     res['qrt'] = True
    #     res['unit'] = True
    #
    # # change this static data to api call
    # res['total'] = 10
    # res['recent'] = [{'start_time': datetime.datetime.now(tz= pytz.UTC), 'end_time': datetime.datetime.now(tz= pytz.UTC)},
    #                  {'start_time': datetime.datetime.now(tz=pytz.UTC), 'end_time': datetime.datetime.now(tz=pytz.UTC)},
    #                  {'start_time': datetime.datetime.now(tz=pytz.UTC), 'end_time': datetime.datetime.now(tz=pytz.UTC)}]
    # return JsonResponse(res, safe=False)
    morcha_data = conn.hgetall(morcha_id)
    if morcha_data.has_key("intrusion"):
        intrusion_id = morcha_data['intrusion']
        intrusion_info = conn.hgetall(intrusion_id)
        morcha_data['intrusion'] = intrusion_info
    return JsonResponse(morcha_data, safe=False)


def delete_intrusions(request):
    morcha_uuids = conn.smembers("morcha_uuid")
    for morcha_id in morcha_uuids:
        intrusion = 'intrusion:' + str(morcha_id)
        conn.delete(intrusion)
        conn.hdel(morcha_id, 'intrusion')
    return HttpResponse()


def detect_intrusion_laser(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-111':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def detect_intrusion_infrared(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-242':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def verify_intrusion_laser(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-111':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc(), "sos": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def verify_intrusion_infrared(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-242':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc(), "sos": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def neutralize_intrusion_laser(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-111':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc(),
                                       "sos": fetch_now_utc(), "neutralized": fetch_now_utc(), "marked_safe": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def neutralize_intrusion_infrared(request):
    morchas = models.Morcha.objects.all()
    for morcha in morchas:
        obj = {
            "repr": 'kvx',
            "location_name": morcha.name,
            "latitude": morcha.geospace.latitude,
            "longitude": morcha.geospace.longitude,
            "last_updated": fetch_now_utc(),
            "uuid": morcha.uuid
        }
        if morcha.name == 'Morcha-242':
            intrusion_key = "intrusion:" + str(morcha.uuid)
            obj['intrusion'] = intrusion_key
            conn.hmset(intrusion_key, {"detected": fetch_now_utc(),
                                       "sos": fetch_now_utc(), "neutralized": fetch_now_utc(), "marked_safe": fetch_now_utc()})
        conn.hmset(morcha.uuid, obj)
    return HttpResponse()


def one_offline(request):
    t = time.time() * 1000
    t -= 300999
    obj = {
        "last_updated": t
    }
    morcha_id = '8d2b5e48-d33f-456f-bd18-138b475dab1f'
    conn.hmset(morcha_id, obj)
    return HttpResponse()


def all_online(request):
    morcha_uuids = conn.smembers("morcha_uuid")

    for morcha_id in morcha_uuids:
        obj = {
            "last_updated": fetch_now_utc()
        }
        conn.hmset(morcha_id, obj)
    return HttpResponse()


def remote(request):
    return render(request, 'remote.html', {})
