from w3fu.storage.documents import Document, Property
from w3fu.storage.collections import Collection, errorsafe, wrapped


class Provider(Document):

    id = Property('_id')
    owner_id = Property('owner_id')
    name = Property('name')

    def _new(self, owner, name):
        self.owner_id = owner.id
        self.name = name

    def writable_by(self, user):
        return self.owner_id == user.id


class Providers(Collection):

    _doc_cls = Provider
    _indexes = [('owner_id', {})]

    @errorsafe
    def update(self, provider):
        return self._collection.update({'_id': provider.id},
                                       {'$set': {'name': provider.name}})

    @wrapped
    @errorsafe
    def find_user(self, user):
        return self._collection.find({'owner_id': user.id})
