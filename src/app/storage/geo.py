from w3fu.storage.documents import Document, Property
from w3fu.storage.collections import Collection, errorsafe, wrapped


class IpRange(Document):

    begin = Property('a')
    end = Property('b')

    def _new(self, begin, end):
        self.begin = begin
        self.end = end

    def has_ip(self, ip):
        return self.begin <= ip <= self.end


class Place(Document):

    id = Property('_id')
    ext_id = Property('ext_id', [])
    name = Property('name')
    pattern = Property('pattern', [])
    region = Property('region')
    district = Property('district')
    ranges = Property('ranges', [])

    def _new(self, ext_id, name, region, district):
        self.ext_id = ext_id
        self.name = name
        self.pattern = name.lower()
        self.region = region
        self.district = district

    def has_ip(self, ip):
        for range in self.ranges:
            if range.has_ip(ip):
                return True
        return False


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

    @wrapped
    @errorsafe
    def find_name(self, name):
        return self._collection.find_one({'pattern': name.lower()})
