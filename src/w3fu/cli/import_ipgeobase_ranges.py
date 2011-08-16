import sys

from w3fu import storage
from w3fu.storage.documents.cities import City

cities = {}
for line in sys.stdin:
    (start, end, _, country, ext_id) = line.split('\t')[:5]
    try:
        ext_id = int(ext_id)
        start = int(start)
        end = int(end)
    except ValueError:
        continue
    cities.setdefault(ext_id, []).append((start, end))
for ext_id, ips in cities.iteritems():
    if not City.replace_ips(storage, ext_id, ips):
        print(ext_id)
