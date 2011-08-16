from w3fu.storage.errors import storagemethod
from w3fu.storage.documents import Document, Property, Identity


class City(Document):

    id = Identity()
    ext_id = Property('ext_id')
    name = Property('name')
    region = Property('region')
    district = Property('district')
    ips = Property('ips', [])

    _indexes = [('ext_id', {'unique': True}),
               ('name', {})]

    @classmethod
    def new(cls, ext_id, name, region, district):
        return cls(ext_id=ext_id, name=name, region=region, district=district)

    @classmethod
    @storagemethod
    def replace_ips(cls, storage, ext_id, ips):
        return cls._c(storage).update({'ext_id': ext_id}, {'$set': {'ips': ips}},
                                      safe=True)['n']
