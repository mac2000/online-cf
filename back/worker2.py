#! /usr/bin/env python3
from __future__ import division # for float point division
import redis
import re
import time
import os

redis_host = os.environ.get('redis') if os.environ.get('redis') else 'localhost'
client = redis.StrictRedis(host=redis_host, port=6379, db=0)

while True:
    if client.llen('qii') != 0:
        pair = client.blpop('qii')[1].decode("utf-8")
        pairReg = re.match(r'(.*):(.*)', pair, re.M|re.I)

        item1 = pairReg.group(1)
        item2 = pairReg.group(2)

        keys1 = client.hkeys('i' + item1)
        keys2 = client.hkeys('i' + item2)

        interCount = 0
        unionCount = 0
        for key in keys1:
            if client.hexists('i' + item2, key):
                interCount += 1
                unionCount += 1
            else:
                unionCount += 1

        for key in keys2:
            if client.hexists('i' + item1, key) != 1:
                unionCount += 1

        if unionCount !=0:
            sim = interCount / unionCount
        else:
            sim = 0

        print ('The similarity of', item1, 'and', item2, 'is', sim)

        client.zadd('s' + item1, -sim, item2)
        client.zadd('s' + item2, -sim, item1)

        maxSize = 10

        # Remove least similar items if similar item set size is larger than maxSize
        for item in [item1, item2]:
            size = client.zcard('s' + item)
            removeCount = size - maxSize
            if removeCount > 0:
                client.zremrangebyrank('s' + item, 0, removeCount - 1)
    else:
        time.sleep(1)
