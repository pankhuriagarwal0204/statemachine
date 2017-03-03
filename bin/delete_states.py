import datetime

import pytz
import redis

con_redis = redis.Redis(host='localhost', db=1)

def main():
    morchas = list(con_redis.smembers('morcha_uuid'))
    for morcha in morchas:
        key = "state:" + str(morcha)
        con_redis.hdel(key, 'state')
        con_redis.hdel(key, 'attempts')
        con_redis.hdel(key, 'start_time')
        con_redis.hdel(key, 'end_time')
    con_redis.delete('last_processed')


if __name__ == '__main__':
    main()