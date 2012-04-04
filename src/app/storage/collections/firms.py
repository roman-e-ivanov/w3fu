from w3fu.storage.collections import Collection, errorsafe, wrapped

from app.storage.documents.firms import Firm


class Firms(Collection):

    _doc_cls = Firm
    _indexes = [('owner_id', {})]

    @errorsafe
    def update(self, firm):
        return self._collection.update({'_id': firm.id},
                                       {'$set': {'name': firm.name}})

    @wrapped
    @errorsafe
    def find_user(self, user):
        return self._collection.find({'owner_id': user.id})
