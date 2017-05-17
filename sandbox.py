#!/usr/bin/python
import redis
import re

r1 = redis.StrictRedis(host='localhost', port=6379, db=0)

# r1.lpush('pageviews_queue', '1:1:1')
#pair = r1.blpop('pageviews_queue')
#pair = pair[1].decode("utf-8")
#print ('pair is', pair)
