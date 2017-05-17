#!/usr/bin/python
import redis
import re

r1 = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
	pair = r1.blpop('pageviews_queue')
	pair = pair[1].decode("utf-8")
	print ('Got new pair', pair)
