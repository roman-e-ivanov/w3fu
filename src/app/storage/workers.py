from w3fu.storage.documents import Document, Property
from w3fu.storage.collections import Collection, errorsafe, wrapped


class Worker(Document):

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name


class Workers(Collection):

    _doc_cls = Worker
    _indexes = [('provider_id', {})]

    @errorsafe
    def update(self, worker):
        return self._collection.update({'_id': worker.id},
                                       {'$set': {'name': worker.name}})

    @wrapped
    @errorsafe
    def find_provider(self, provider_id):
        return self._collection.find({'provider_id': provider_id})
