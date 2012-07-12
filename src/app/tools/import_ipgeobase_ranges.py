#!/usr/bin/python

import sys

from app.storage.geo import IpRange, Place


range_by_id = {}
for line in sys.stdin:
    (begin, end, _, country, ext_id) = line.split('\t')[:5]
    try:
        ext_id = int(ext_id)
        begin = int(begin)
        end = int(end)
    except ValueError:
        continue
    range_by_id.setdefault(ext_id, []).append(IpRange.new(begin, end))
for ext_id, ranges in range_by_id.iteritems():
    if not Place.replace_ranges(ext_id, ranges):
        print(ext_id)
