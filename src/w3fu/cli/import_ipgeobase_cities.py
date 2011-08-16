import sys
import codecs

from w3fu import storage
from w3fu.storage.documents.cities import City


for line in codecs.getreader('cp1251')(sys.stdin):
    (ext_id, name, region, district) = line.split('\t')[:4]
    try:
        ext_id = int(ext_id)
    except ValueError:
        continue
    city = City.new(ext_id, name, region, district)
    if City.insert(storage, city):
        print('\t'.join([str(ext_id), name, region, district]))
