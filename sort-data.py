import json
import time
import csv
from pprint import pprint
import operator

majors = {}


# def get_length(data-csv):


rows = []
with open('data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rows.append(row)
del rows[0]
rows = sorted(rows)
with open('data-sorted.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name','value'])
    for row in rows:
        writer.writerow(row)
