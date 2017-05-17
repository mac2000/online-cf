#!/usr/bin/python
import redis
import re

r1 = redis.StrictRedis(host='localhost', port=6379, db=0)

r1.lpush('pageviews_queue', '1:1:1')
