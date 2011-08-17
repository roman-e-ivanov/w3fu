from w3fu.storage.errors import storagemethod
from w3fu.storage.documents import Document, Property, Identity


class City(Document):

    id = Identity()
    ext_id = Property('ext_id', [])
    name = Property('name')
    pattern = Property('pattern', [])
    region = Property('region')
    district = Property('district')
    ips = Property('ips', [])

    _indexes = [('ext_id', {'unique': True}),
               ('pattern', {}),
               ('ips.a', {})]

    @classmethod
    def new(cls, ext_id, name, region, district):
        return cls(ext_id=ext_id, name=name, pattern=name.lower(),
                   region=region, district=district)

    @classmethod
    @storagemethod
    def replace_ips(cls, storage, ext_id, ips):
        return cls._c(storage).update({'ext_id': ext_id}, {'$set': {'ips': ips}},
                                      safe=True)['n']

    @classmethod
    @storagemethod
    def find_ip(cls, storage, ip):
        return cls._c(storage).find_one({'ips.a': {'$lte': ip}},
                                        as_class=cls).sort('ips.a', -1)

    @classmethod
    @storagemethod
    def find_name_prefix(cls, storage, prefix):
        return cls._c(storage).find({'pattern': {'$regex': '^' + prefix.lower()}},
                                    as_class=cls).sort('pattern').limit(10)
