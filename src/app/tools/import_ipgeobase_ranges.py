import sys

from app.storage import storage
from app.storage.documents.geo import IpRange


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
for ext_id, ranges in places.iteritems():
    if not storage.places.replace_ranges(ext_id, ranges):
        print(ext_id)
