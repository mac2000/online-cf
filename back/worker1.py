#! /usr/bin/env python3
import redis
import re
import time
import os

redis_host = os.environ.get('redis') if os.environ.get('redis') else 'localhost'
client = redis.StrictRedis(host=redis_host, port=6379, db=0)

while True:
    #There must be a list named 'qiu' in r1 first
    if client.llen('qiu') != 0:
        pair = client.blpop('qiu')
        print ('pair is', pair[1].decode("utf-8"))
        pair = pair[1].decode("utf-8")

        # Parse item and user names
        # item:user:rating
        pairReg = re.match(r'(.*):(.*):(.*)', pair, re.M|re.I)

        item = pairReg.group(1)
        user = pairReg.group(2)
        rating = pairReg.group(3)

        # Add the user to item's set in r2
        client.hset('i' + item, user, rating)

        # Add the item to user's set in r4
        client.sadd('u' + user, item)

        # Put all item:alsowatcheditem pairs to qii
        commonItems = client.smembers('u' + user)
        while len(commonItems) != 0:
            commonItem = commonItems.pop().decode("utf-8")
            if commonItem != item:
                itemPair = item + ':' + commonItem
                print('Calculate the similarity of', item, commonItem, 'pair')
                client.lpush('qii', itemPair)
    else:
        time.sleep(1)
