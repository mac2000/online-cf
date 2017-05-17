#! /usr/bin/env python3
import redis
import sys
import time

item = 1;
if len(sys.argv) == 2:
    item = sys.argv[1];

print('Showing the most similar items for', item)

r3 = redis.StrictRedis(host='r3', port=6379, db=0)

while True:
    similars = r3.zrange(item, 0, -1, desc=False, withscores=True)
    print (list(map(lambda e: [e[0].decode('utf-8'), "{:.3f}".format(-e[1])], similars)))
    time.sleep(1)
