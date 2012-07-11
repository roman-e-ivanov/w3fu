from w3fu.storage import safe, Property

from app.storage import Model


class Service(Model):

    _collection = 'services'
    _indexes = [('provider_id', {})]

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name

    @classmethod
    @safe()
    def update(cls, service):
        return cls._c().update({'_id': service.id},
                               {'$set': {'name': service.name}})

    @classmethod
    @safe(True)
    def find_provider(cls, provider_id):
        return cls._c().find({'provider_id': provider_id})
