#!/usr/bin/python
import csv
import urllib.request

with open('C:/Users/AlexandrM/Desktop/online-cf/data/merged.csv') as csvread:
    for row in csv.DictReader(csvread):
        urllib.request.urlopen("http://localhost:3000/item/" + row['item'] + '/user/' + row['user'] + '/rating/' + row['rating']).read()

print('Executed all requests.')
