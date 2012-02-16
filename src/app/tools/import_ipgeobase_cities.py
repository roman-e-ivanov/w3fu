#!/usr/bin/python

import sys
import codecs

from w3fu.storage.base import Database

from app import config

from app.storage.collections.geo import Places
from app.storage.documents.geo import Place


database = Database(config.db_uri, config.db_name)
places = Places(database)

for line in codecs.getreader('cp1251')(sys.stdin):
    (ext_id, name, region, district) = line.split('\t')[:4]
    try:
        ext_id = int(ext_id)
    except ValueError:
        continue
    place = Place.new(places, ext_id, name, region, district)
    if place.insert():
        print('\t'.join([str(ext_id), name, region, district]))
