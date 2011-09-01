from w3fu.storage.documents import Document, Property, Identity


class IpRange(Document):

    begin = Property('a')
    end = Property('b')

    def _new(self, begin, end):
        self.begin = begin
        self.end = end

    def has_ip(self, ip):
        return self.begin <= ip <= self.end


class Place(Document):

    id = Identity()
    ext_id = Property('ext_id', [])
    name = Property('name')
    pattern = Property('pattern', [])
    region = Property('region')
    district = Property('district')
    ranges = Property('ips', [])

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
