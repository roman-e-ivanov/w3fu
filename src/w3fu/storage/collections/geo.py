from w3fu.storage.documents.geo import Place
from w3fu.storage.collections import Collection, errorsafe, wrapped


class Places(Collection):

    _doc_cls = Place
    _indexes = [('ext_id', {'unique': True}),
               ('pattern', {}),
               ('ranges.a', {})]

    @errorsafe
    def replace_ranges(self, ext_id, ranges):
        raw = [range.raw for range in ranges]
        return self._collection.update({'ext_id': ext_id}, {'$set': {'ranges': raw}},
                                       safe=True)['n']

    @wrapped
    @errorsafe
    def find_ip(self, ip):
        doc = self._collection.find_one({'ips.a': {'$lte': ip}}).sort('ranges.a', -1)
        if doc is not None and doc.has_ip(ip):
            return doc
        return None

    @wrapped
    @errorsafe
    def find_pattern(self, pattern):
        return self._collection.find({'pattern': {'$regex': '^' + pattern.lower()}}
                                     ).sort('pattern').limit(10)
