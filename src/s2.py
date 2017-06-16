#! /usr/bin/env python3
import redis
import re
import time

r1 = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
    #There must be a list named 'qiu' in r1 first
    if r1.llen('qiu') != 0:
        pair = r1.blpop('qiu')
        print ('pair is', pair[1].decode("utf-8"))
        pair = pair[1].decode("utf-8")

        # Parse item and user names
        # item:user:rating
        pairReg = re.match(r'(.*):(.*):(.*)', pair, re.M|re.I)

        item = pairReg.group(1)
        user = pairReg.group(2)
        rating = pairReg.group(3)

        # Add the user to item's set in r2
        r1.hset('i' + item, user, rating)

        # Add the item to user's set in r4
        r1.sadd('u' + user, item)

        # Put all item:alsowatcheditem pairs to qii
        commonItems = r1.smembers('u' + user)
        while len(commonItems) != 0:
            commonItem = commonItems.pop().decode("utf-8")
            if commonItem != 'i' + item:
                itemPair = item + ':' + commonItem
                print('Calculate the similarity of', item, commonItem, 'pair')
                r1.lpush('qii', itemPair)
    else:
        time.sleep(1)
