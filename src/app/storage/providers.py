from w3fu.storage.documents import Document, Property
from w3fu.storage.collections import Collection, errorsafe, wrapped


class Provider(Document):

    id = Property('_id')
    name = Property('name')

    def _new(self, name):
        self.name = name


class Providers(Collection):

    _doc_cls = Provider

    @errorsafe
    def update(self, provider):
        return self._collection.update({'_id': provider.id},
                                       {'$set': {'name': provider.name}})

    @wrapped
    @errorsafe
    def find_from_user(self, user):
        return self._collection.find({'_id': {'$in': user.owned}})
