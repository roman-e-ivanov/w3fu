import sys

from w3fu import storage
from w3fu.storage.documents.geo import IpRange

places = {}
for line in sys.stdin:
    (begin, end, _, country, ext_id) = line.split('\t')[:5]
    try:
        ext_id = int(ext_id)
        begin = int(begin)
        end = int(end)
    except ValueError:
        continue
    places.setdefault(ext_id, []).append(IpRange.new(storage.places, begin, end))
for ext_id, ips in places.iteritems():
    if not storage.places.replace_ips(ext_id, ips):
        print(ext_id)
