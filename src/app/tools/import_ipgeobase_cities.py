#!/usr/bin/python

import sys
import codecs

from w3fu import storage

from app import config
from app.storage import geo


storage.Database.push(uri=config.db_uri, dbname=config.db_name)

for line in codecs.getreader('cp1251')(sys.stdin):
    (ext_id, name, region, district) = line.split('\t')[:4]
    try:
        ext_id = int(ext_id)
    except ValueError:
        continue
    place = geo.Place.new(ext_id, name, region, district)
    if geo.Place.insert():
        print('\t'.join([str(ext_id), name, region, district]))
