from w3fu.storage import safe, Property, ListContainer

from app.storage import Model


class Worker(Model):

    _collection = 'workers'
    _indexes = [('provider_id', {})]

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name

    @classmethod
    @safe()
    def update(cls, worker):
        return cls._c().update({'_id': worker.id},
                               {'$set': {'name': worker.name}})

    @classmethod
    @safe(True)
    def find_provider(cls, provider_id):
        return cls._c().find({'provider_id': provider_id})
