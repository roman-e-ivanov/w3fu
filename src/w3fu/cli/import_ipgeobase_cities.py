import sys
import codecs

from w3fu import storage
from w3fu.storage.documents.geo import Place


for line in codecs.getreader('cp1251')(sys.stdin):
    (ext_id, name, region, district) = line.split('\t')[:4]
    try:
        ext_id = int(ext_id)
    except ValueError:
        continue
    place = Place.new(storage.places, ext_id, name, region, district)
    if place.insert():
        print('\t'.join([str(ext_id), name, region, district]))
