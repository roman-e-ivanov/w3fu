from w3fu.storage import safe, Property

from app.storage import Model


class Provider(Model):

    _collection = 'providers'

    id = Property('_id')
    name = Property('name')

    def _new(self, name):
        self.name = name

    @classmethod
    @safe()
    def update(cls, provider):
        return cls._c().update({'_id': provider.id},
                               {'$set': {'name': provider.name}})

    @classmethod
    @safe(True)
    def find_from_user(cls, user):
        return cls._c().find({'_id': {'$in': user.owned}})
