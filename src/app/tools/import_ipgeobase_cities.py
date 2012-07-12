#!/usr/bin/python

import sys
import codecs

from app.storage.geo import Place


for line in codecs.getreader('cp1251')(sys.stdin):
    (ext_id, name, region, district) = line.split('\t')[:4]
    try:
        ext_id = int(ext_id)
    except ValueError:
        continue
    place = Place.new(ext_id, name, region, district)
    if Place.insert():
        print('\t'.join([str(ext_id), name, region, district]))
