#!/usr/bin/python
import csv
import socket

with open('/code/data/merged.csv') as csvread:
    for row in csv.DictReader(csvread):
        requeststr = 'HTTP GET /item/:'+row['movieId']+'/user/:'+row['userId']+'/rat/:'+row['rating']
        print ('requesting ' + requeststr)

        s = socket.socket()
        s.connect(('s1', 8080))
        s.send(bytearray(requeststr,'UTF-8'))
        s.close

print('Executed all requests.')
