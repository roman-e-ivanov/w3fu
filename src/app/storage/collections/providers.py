from w3fu.storage.collections import Collection, errorsafe, wrapped

from app.storage.documents.providers import Provider


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
