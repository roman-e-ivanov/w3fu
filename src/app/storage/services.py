from w3fu.storage.documents import Document, Property
from w3fu.storage.collections import Collection, errorsafe, wrapped


class Service(Document):

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name


class Services(Collection):

    _doc_cls = Service
    _indexes = [('provider_id', {})]

    @errorsafe
    def update(self, service):
        return self._collection.update({'_id': service.id},
                                       {'$set': {'name': service.name}})

    @wrapped
    @errorsafe
    def find_provider(self, provider_id):
        return self._collection.find({'provider_id': provider_id})
