from w3fu import storage


class Worker(storage.Model):

    _collection = 'workers'
    _indexes = [('provider_id', {})]

    id = storage.Property('_id')
    provider_id = storage.Property('provider_id')
    name = storage.Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name

    @classmethod
    @storage.safe()
    def update(cls, worker):
        return cls._c().update({'_id': worker.id},
                               {'$set': {'name': worker.name}})

    @classmethod
    @storage.safe(True)
    def find_provider(cls, provider_id):
        return cls._c().find({'provider_id': provider_id})
